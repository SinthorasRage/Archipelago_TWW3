from CommonClient import CommonContext, ClientCommandProcessor, server_loop, get_base_parser, gui_enabled, logger
import Utils
import asyncio
import colorama
import logging
import copy
from worlds.tww3.settlements import lord_name_to_faction_dict
from .item_tables.items import ItemType
from .item_tables.progression_filler_table import progression_table, filler_table
from .item_tables.unique_item_table import unique_item_table
from .item_tables.progressive_buildings_table import progressive_buildings_table
from .item_tables.progressive_units_table import progressive_units_table
from worlds.tww3.locations import location_table
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch as launch_component
import io
import os

path = "."

class TWW3CommandProcessor(ClientCommandProcessor):    
    def _cmd_spheres(self):
        if isinstance(self.ctx, TWW3Context):
            sorted_spheres = dict(sorted(self.ctx.spheres.items(), key=lambda item: item[1], reverse=True))
            for faction, reqSphere in sorted_spheres.items():
                logger.info("Faction: " + faction + " " + str(reqSphere) + " spheres")

    def _cmd_capitals(self):
        if isinstance(self.ctx, TWW3Context):
            for faction, capital in self.ctx.capitals.items():
                logger.info("Faction: " + faction + " Capital: " + capital)

class WaaaghMessenger:
    def __init__(self, path):
        self.file = open(path, 'w+')

    def run(self, message):
        self.file.write(message + '\n')

    def flush(self):    
        self.file.flush()

class WaaaghWatcher:
    def __init__(self, path, context):
        self.file = open(path, 'w+')
        self.context = context

    async def watch(self):
        print('Watching for Waaagh...')
        self.file.seek(0, 2)
        while True:
            line = self.file.readline()
            if not line:
                await asyncio.sleep(0.5)
                continue
            logger.info("Sending Location " + line.strip())
            await self.context.check(line.strip())

class TWW3Context(CommonContext):
    game = 'Total War Warhammer 3'
    command_processor = TWW3CommandProcessor
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.initialized = False
        self.path = None
        self.numberOfGoalItems = 0
        self.numberOfSphereItems = 0
        self.item_table = dict(progression_table)
        self.item_table.update(filler_table)
        self.item_table.update(unique_item_table)
        self.item_table.update(progressive_buildings_table)
        self.item_table.update(progressive_units_table)
        self.progressive_items_flags = {key: 0 for key in self.item_table.keys()}

    # def make_gui(self) -> "type[kvui.GameManager]":
    #     """
    #     To return the Kivy `App` class needed for `run_gui` so it can be overridden before being built

    #     Common changes are changing `base_title` to update the window title of the client and
    #     updating `logging_pairs` to automatically make new tabs that can be filled with their respective logger.

    #     ex. `logging_pairs.append(("Foo", "Bar"))`
    #     will add a "Bar" tab which follows the logger returned from `logging.getLogger("Foo")`
    #     """
    #     from kvui import GameManager

    #     class TextManager(GameManager):
    #         base_title = "TWW3 Client"

    #     return TextManager

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TWW3Context, self).server_auth(password_requested)
        await self.get_username()
        await self.get_path()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.on_connected(args)
        elif cmd == "ReceivedItems":
            self.on_received_items(args)

    def on_connected(self, args: dict): 
        self.waaaghWatcher = WaaaghWatcher(self.path + '\\engine.out', self)
        waaaghWatcher_task = asyncio.create_task(self.waaaghWatcher.watch(), name='WaaaghWatcher')
        self.waaaghMessenger = WaaaghMessenger(self.path + '\\engine.in')
        self.settlements = args['slot_data']['Settlements']
        self.locationLookup = dict()
        for key, entry in location_table.items():
            self.locationLookup[entry['name']] = int(key)
        self.playerFaction = lord_name_to_faction_dict[args['slot_data']['PlayerFaction']]
        logger.info("The Player Faction is: " + self.playerFaction)
        self.randitemList = args['slot_data']['Items']
        self.goalNumber = args['slot_data']['DominationGoal']
        self.spheres = args['slot_data']['Spheres']
        self.capitals = args['slot_data']['FactionCapitals']
        self.progressiveBuildings = args['slot_data']['ProgressiveBuildings']
        self.progressiveUnits = args['slot_data']['ProgressiveUnits']
        self.startingTier = args['slot_data']['StartingTier']
        #EngineInitializer.initialize(self.settlements, self.randitemList, self.playerFaction, self.spheres, self.capitals, self.waaaghMessenger)
        EngineInitializer.initialize(self)

    def on_received_items(self, args: dict):
        # for entry in self.items_received:
        for entry in args["items"]:
            item = self.item_table[entry.item]
            sender = "You" if entry.player == self.slot else f"Player {entry.player}"
            logger.info(f"From: {sender} | Item: {item.name}")
            if item.type == ItemType.building:
                if (self.progressiveBuildings == True):
                    self.send_next_progressive_building(item.name)
                else:
                    self.waaaghMessenger.run("cm:remove_event_restricted_building_record_for_faction(\"%s\", \"%s\")" % (item.name, self.playerFaction))
            elif item.type == ItemType.tech:
                self.waaaghMessenger.run("cm:unlock_technology(\"%s\", \"%s\")" % (self.playerFaction, item.name))
            elif item.type == ItemType.unit:
                if (self.progressiveUnits == True):
                    self.send_next_progressive_units(item.name)
                else:
                    self.waaaghMessenger.run("cm:remove_event_restricted_unit_record_for_faction(\"%s\", \"%s\")" % (item.name, self.playerFaction))
            elif item.type == ItemType.goal:
                self.numberOfGoalItems = self.numberOfGoalItems + 1
                logger.info("You now have: " + str(self.numberOfGoalItems) + "/" + str(self.goalNumber) + " Orbs of Domination" )
            elif item.type == ItemType.progression:
                self.numberOfSphereItems = self.numberOfSphereItems + 1
                self.triggerProgressionEvents(self.numberOfSphereItems)
                logger.info("You now have: " + str(self.numberOfSphereItems) + " Spheres of Influence" )
            elif item.type == ItemType.filler:
                if item.name == "Gold":
                    self.waaaghMessenger.run("cm:treasury_mod(\"%s\", 10000)" % (self.playerFaction))

        if self.numberOfGoalItems == self.goalNumber:
            asyncio.create_task(self.send_msgs([{"cmd": "StatusUpdate", "status": 30}]))
        self.waaaghMessenger.flush()

    def send_next_progressive_building(self, progressionGroup):
        for id, item in self.item_table.items():
            if ((item.faction == self.playerFaction) and (item.progressionGroup == progressionGroup) and (self.progressive_items_flags[id] == 0)):
                self.progressive_items_flags[id] = 1
                self.waaaghMessenger.run("cm:remove_event_restricted_building_record_for_faction(\"%s\", \"%s\")" % (item.name, self.playerFaction))
                return
        raise Exception("Progressive Building " + progressionGroup + " not found in item_table")
    
    def send_next_progressive_units(self, progressionGroup):
        # The Amount of progressive Items per Group is saved on the first index with that progression Group
        for id, item in self.item_table.items():
            if ((item.faction == self.playerFaction) and (item.progressionGroup == progressionGroup)):
                level_to_unlock = self.progressive_items_flags[id]
                self.progressive_items_flags[id] += 1
                break
        for id, item in self.item_table.items():
            if ((item.faction == self.playerFaction) and (item.progressionGroup == progressionGroup) and (item.tier == level_to_unlock)):
                self.waaaghMessenger.run("cm:remove_event_restricted_unit_record_for_faction(\"%s\", \"%s\")" % (item.name, self.playerFaction))

    def triggerProgressionEvents(self, numberOfSphereItems):
        oldSphere = []
        newSphere = []
        allOthers = []
        for faction, sphere in self.spheres.items():
            if sphere < numberOfSphereItems:
                oldSphere.append(faction)
            elif sphere == numberOfSphereItems:
                newSphere.append(faction)
            else:
                allOthers.append(faction)
        for oldFaction in oldSphere:
            for newFaction in newSphere:
                self.waaaghMessenger.run("cm:force_diplomacy(\"faction:%s\", \"faction:%s\", \"all\", true, true, true)" % (oldFaction, newFaction))
        for newFaction in newSphere:
            for otherFaction in allOthers:
                self.waaaghMessenger.run("cm:force_make_peace(\"%s\", \"%s\")" % (newFaction, otherFaction))
                self.waaaghMessenger.run("cm:force_diplomacy(\"faction:%s\", \"faction:%s\", \"all\", false, false, true)" % (newFaction, otherFaction))
        return

    async def check(self, location):
        await self.check_locations([self.locationLookup[location]])

    async def get_path(self):
        if not self.path:
            logger.info('Enter TWW3 Installation path:')
            self.path = await self.console_input()
            logger.info('Accepted Path is: ' + self.path)
            if not path or not os.path.exists(self.path):
                logger.error('Path does not point to a directory')
            if not os.path.isfile(self.path + '\\Warhammer3.exe'):
                logger.error('No TWW3 exe in Path')
            else:
                logger.info('Found TWW3 exe')

    def run_gui(self):
        from kvui import GameManager

        class TWW3Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago " + self.game + " Client"

        self.ui = TWW3Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

class EngineInitializer():

    @classmethod
    # def initialize(cls, settlements, randitem_list, playerFaction, spheres, capitals, waaaghMessenger):
    def initialize(cls, context):
        settlements = context.settlements
        randitem_list = context.randitemList
        playerFaction = context.playerFaction
        spheres = context.spheres
        capitals = context.capitals
        startingTier = context.startingTier
        waaaghMessenger = context.waaaghMessenger
        for settlement, faction in settlements.items():
            waaaghMessenger.run("cm:transfer_region_to_faction(\"%s\", \"%s\")" % (settlement, faction))
        for faction, settlement in capitals.items():
            waaaghMessenger.run("teleport_all_heroes_of_faction_to_region(\"%s\", \"%s\")" % (faction, settlement))
            waaaghMessenger.run("teleport_all_lords_of_faction_to_region(\"%s\", \"%s\")" % (faction, settlement))
        for itemNumber in randitem_list:
            itemData = context.item_table[itemNumber]
            if itemData.type == ItemType.tech:
                waaaghMessenger.run("cm:lock_one_technology_node(\"%s\", \"%s\")" % (playerFaction, itemData.name))
            elif ((itemData.type == ItemType.building) and (context.progressiveBuildings == False) and (itemData.progressionGroup != None)):
                waaaghMessenger.run("cm:add_event_restricted_building_record_for_faction(\"%s\", \"%s\")" % (itemData.name, playerFaction))
            elif ((itemData.type == ItemType.unit) and (context.progressiveUnits == False) and (itemData.progressionGroup != None)):
                waaaghMessenger.run("cm:add_event_restricted_unit_record_for_faction(\"%s\", \"%s\")" % (itemData.name, playerFaction))
        if (context.progressiveBuildings == True):
            cls.lock_progressive_buildings(playerFaction, startingTier, waaaghMessenger, context.item_table, context.progressive_items_flags)
        if (context.progressiveUnits == True):
            cls.lock_progressive_units(playerFaction, startingTier, waaaghMessenger, context.item_table, context.progressive_items_flags)
        sphereZeroFactions = []
        sphereAllOthers = []
        for faction, sphere in spheres.items():
            if sphere == 0:
                sphereZeroFactions.append(faction)
            else:
                sphereAllOthers.append(faction)
            continue
        for factionZero in sphereZeroFactions:
            for faction in sphereAllOthers:
                waaaghMessenger.run("cm:force_make_peace(\"%s\", \"%s\")" % (factionZero, faction))
                waaaghMessenger.run("cm:force_diplomacy(\"faction:%s\", \"faction:%s\", \"all\", false, false, true)" % (factionZero, faction))
        waaaghMessenger.flush()

    def lock_progressive_buildings(playerFaction, startingTier, waaaghMessenger, item_table, progressive_items_flags):
        for id, item in item_table.items():
            if ((item.faction == playerFaction) and (item.type == ItemType.building) and (item.progressionGroup != None)):
                if (item.tier + 1 > startingTier):
                    waaaghMessenger.run("cm:add_event_restricted_building_record_for_faction(\"%s\", \"%s\")" % (item.name, playerFaction))
                else:
                    progressive_items_flags[id] = 1

    def lock_progressive_units(playerFaction, startingTier, waaaghMessenger, item_table, progressive_items_flags):
        for id, item in item_table.items():
            if ((item.faction == playerFaction) and (item.type == ItemType.unit) and (item.progressionGroup != None)):
                # The Amount of progressive Items per Group is saved on the first index with that progression Group, but since we don't know the first item of each progression Group, we set all items to the starting Tier for now.
                progressive_items_flags[id] = startingTier + 1
                if (item.tier > startingTier):
                    waaaghMessenger.run("cm:add_event_restricted_unit_record_for_faction(\"%s\", \"%s\")" % (item.name, playerFaction))

def launch(*launch_args: str):
    Utils.init_logging('TWW3Client')
    logging.getLogger().setLevel(logging.INFO)

    async def main(args):
        ctx = TWW3Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name='ServerLoop')

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None
        await ctx.shutdown()

    parser = get_base_parser()
    args = parser.parse_args()
    colorama.just_fix_windows_console()

    asyncio.run(main(args))
    colorama.deinit()

if __name__ == '__main__':
    launch(*args)
    # Utils.init_logging('TWW3Client')
    # logging.getLogger().setLevel(logging.INFO)

    # async def main(args):
    #     ctx = TWW3Context(args.connect, args.password)
    #     ctx.server_task = asyncio.create_task(server_loop(ctx), name='ServerLoop')

    #     if gui_enabled:
    #         ctx.run_gui()
    #     ctx.run_cli()

    #     await ctx.exit_event.wait()
    #     ctx.server_address = None
    #     await ctx.shutdown()

    # parser = get_base_parser()
    # args = parser.parse_args()
    # colorama.just_fix_windows_console()

    # asyncio.run(main(args))
    # colorama.deinit()