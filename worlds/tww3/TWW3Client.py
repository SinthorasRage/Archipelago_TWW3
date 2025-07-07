from CommonClient import CommonContext, ClientCommandProcessor, server_loop, get_base_parser, gui_enabled, logger
import Utils
import asyncio
import colorama
import logging
import copy
from worlds.tww3.settlements import lord_name_to_faction_dict
from worlds.tww3.items import item_table, ItemType
from worlds.tww3.locations import location_table
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch as launch_component
import io
import os

path = "."

class TWW3CommandProcessor(ClientCommandProcessor):
    pass

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

    def make_gui(self) -> "type[kvui.GameManager]":
        """
        To return the Kivy `App` class needed for `run_gui` so it can be overridden before being built

        Common changes are changing `base_title` to update the window title of the client and
        updating `logging_pairs` to automatically make new tabs that can be filled with their respective logger.

        ex. `logging_pairs.append(("Foo", "Bar"))`
        will add a "Bar" tab which follows the logger returned from `logging.getLogger("Foo")`
        """
        from kvui import GameManager

        class TextManager(GameManager):
            base_title = "TWW3 Client"

        return TextManager

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
        EngineInitializer.initialize(self.settlements, self.randitemList, self.playerFaction, self.spheres, self.waaaghMessenger)

    def on_received_items(self, args: dict):
        numberOfGoalItems = 0
        numberOfSphereItems = 0
        # for entry in self.items_received:
        print("Args ist: ")
        print(args)
        for entry in args["items"]:
            print("entry " + str(entry))
            item = item_table[entry.item]
            sender = "You" if entry.player == self.slot else f"Player {entry.player}"
            logger.info(f"From: {sender} | Item: {item.name}")
            if item.type == ItemType.building:
                self.waaaghMessenger.run("cm:remove_event_restricted_building_record_for_faction(\"%s\", \"%s\")" % (item.name, self.playerFaction))
            elif item.type == ItemType.tech:
                self.waaaghMessenger.run("cm:unlock_technology(\"%s\", \"%s\")" % (self.playerFaction, item.name))
            elif item.type == ItemType.unit:
                self.waaaghMessenger.run("cm:remove_event_restricted_unit_record_for_faction(\"%s\", \"%s\")" % (item.name, self.playerFaction))
            elif item.type == ItemType.goal:
                numberOfGoalItems = numberOfGoalItems + 1
                logger.info("You now have: " + str(numberOfGoalItems) + "/" + str(self.goalNumber) + " Orbs of Domination" )
            elif item.type == ItemType.progression:
                numberOfSphereItems = numberOfSphereItems + 1
                self.triggerProgressionEvents(numberOfSphereItems)
            elif item.type == ItemType.filler:
                if item.name == "Gold":
                    self.waaaghMessenger.run("cm:treasury_mod(\"%s\", 10000)" % (self.playerFaction))

        if numberOfGoalItems == self.goalNumber:
            asyncio.create_task(self.send_msgs([{"cmd": "StatusUpdate", "status": 30}]))
        self.waaaghMessenger.flush()

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

    def on_print_json(self, args: dict):
        pass #print(args)

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
    def initialize(cls, settlements, randitem_list, playerFaction, spheres, waaaghMessenger):
        for settlement, faction in settlements.items():
            waaaghMessenger.run("cm:transfer_region_to_faction(\"%s\", \"%s\")" % (settlement, faction))
            waaaghMessenger.run("teleport_all_heroes_of_faction_to_region(\"%s\", \"%s\")" % (faction, settlement))
            waaaghMessenger.run("teleport_all_lords_of_faction_to_region(\"%s\", \"%s\")" % (faction, settlement))
        for itemNumber in randitem_list:
            itemData = item_table[itemNumber]
            if itemData.type == ItemType.tech:
                waaaghMessenger.run("cm:lock_one_technology_node(\"%s\", \"%s\")" % (playerFaction, itemData.name))
            elif itemData.type == ItemType.building:
                waaaghMessenger.run("cm:add_event_restricted_building_record_for_faction(\"%s\", \"%s\")" % (itemData.name, playerFaction))
            elif itemData.type == ItemType.unit:
                waaaghMessenger.run("cm:add_event_restricted_unit_record_for_faction(\"%s\", \"%s\")" % (itemData.name, playerFaction))
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