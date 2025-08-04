from CommonClient import CommonContext, ClientCommandProcessor, server_loop, get_base_parser, gui_enabled, logger
import Utils
import asyncio
import colorama
import logging
from .locations_table.settlements import lord_name_to_faction_dict
from .item_tables.items import ItemType
from .item_tables.progression_table import progression_table
from .item_tables.filler_item_table import filler_weak_table, filler_strong_table, trap_harmless_table, trap_weak_table, trap_strong_table
from .item_tables.effect_table import global_effect_table
from .item_tables.ancillaries_table import ancillaries_regular_table, ancillaries_legendary_table
from .item_tables.unique_item_table import unique_item_table
from .item_tables.progressive_buildings_table import progressive_buildings_table
from .item_tables.progressive_units_table import progressive_units_table
from .item_tables.ritual_table import ritual_table
from .item_tables.progressive_techs_table import progressive_techs_table
from .filler_item_manager import Filler_Item_Manager
from .locations_table.locations import location_table
from . import TWW3World
from worlds.LauncherComponents import launch as launch_component
import os

path = "."

class TWW3CommandProcessor(ClientCommandProcessor):    
    def _cmd_spheres(self):
        """Prints a list of settlements and sphere requirements."""
        if isinstance(self.ctx, TWW3Context):
            sorted_spheres = dict(sorted(self.ctx.spheres.items(), key=lambda item: item[1], reverse=True))
            for faction, reqSphere in sorted_spheres.items():
                if reqSphere <= self.ctx.numberOfSphereItems:
                    logger.info("Faction: " + faction + " " + str(reqSphere) + " spheres")

    def _cmd_toggleTraps(self):
        """Turn Traps off and on."""
        if isinstance(self.ctx, TWW3Context):
            if self.ctx.are_traps_enabled == True:
                self.ctx.are_traps_enabled = False
                logger.info("Traps are now turned off.")
            elif self.ctx.are_traps_enabled == False:
                self.ctx.are_traps_enabled = True
                logger.info("Traps are now turned on.")

    def _cmd_capitals(self):
        """Prints a list of starting Capitals."""
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
    are_traps_enabled = True

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.initialized = False
        self.item_table = dict(progression_table)
        self.item_table.update(filler_weak_table)
        self.item_table.update(filler_strong_table)
        self.item_table.update(global_effect_table)
        self.item_table.update(ancillaries_regular_table)
        self.item_table.update(ancillaries_legendary_table)
        self.item_table.update(trap_harmless_table)
        self.item_table.update(trap_weak_table)
        self.item_table.update(trap_strong_table)
        self.item_table.update(unique_item_table)
        self.item_table.update(progressive_buildings_table)
        self.item_table.update(progressive_units_table)
        self.item_table.update(progressive_techs_table)
        self.item_table.update(ritual_table)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TWW3Context, self).server_auth(password_requested)
        await self.get_username()
#        await self.get_path()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.on_connected(args)
        elif cmd == "ReceivedItems":
            self.on_received_items(args)

    def on_connected(self, args: dict):
        self.path = TWW3World.settings.tww3_path
        self.progressive_items_flags = {key: 0 for key in self.item_table.keys()}
        if not self.path or not os.path.exists(self.path):
            logger.error('Path does not point to a directory. Please remove Path from host.yaml. If you need help, ask in the Discord channel.')
        if not os.path.isfile(self.path + '\\Warhammer3.exe'):
            logger.error('No TWW3 exe in Path. Please remove Path from host.yaml. If you need help, ask in the Discord channel.')
        self.numberOfGoalItems = 0
        self.numberOfSphereItems = 0
        self.waaaghWatcher = WaaaghWatcher(self.path + '\\engine.out', self)
        waaaghWatcher_task = asyncio.create_task(self.waaaghWatcher.watch(), name='WaaaghWatcher')
        self.waaaghMessenger = WaaaghMessenger(self.path + '\\engine.in')
        self.settlements = args['slot_data']['Settlements']
        self.hordes = args['slot_data']['Hordes']
        self.locationLookup = dict()
        for key, entry in location_table.items():
            self.locationLookup[entry['name']] = int(key)
        self.playerFaction = lord_name_to_faction_dict[args['slot_data']['PlayerFaction']]
        logger.info("The Player Faction is: " + self.playerFaction)
        self.randitemList = args['slot_data']['Items']
        self.goalNumber = args['slot_data']['DominationGoal']
        self.spheres = args['slot_data']['Spheres']
        self.capitals = args['slot_data']['FactionCapitals']
        self.progressiveTechs = args['slot_data']['ProgressiveTechs']
        self.progressiveBuildings = args['slot_data']['ProgressiveBuildings']
        self.progressiveUnits = args['slot_data']['ProgressiveUnits']
        self.startingTier = args['slot_data']['StartingTier']
        self.shuffleRituals = args['slot_data']['Ritual_Shuffle']
        self.randomizePersonalities = args['slot_data']['RandomizePersonalities']
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
                if (self.progressiveTechs == True):
                    self.send_next_progressive_tech(item.name)
                else:
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
            elif item.type == ItemType.filler_weak:
                if item.name == "Get-Rich-Quick Scroll":
                    self.waaaghMessenger.run("cm:treasury_mod(\"%s\", cm:random_number(10000,1))" % (self.playerFaction))
                elif item.name == "Handfull of Order" :
                    self.waaaghMessenger.run("set_random_positive_public_order()")
                elif item.name == "The GroBro 3000™":
                    self.waaaghMessenger.run("add_random_growth_to_player()")
            elif (item.type == ItemType.ancillaries_regular) or (item.type == ItemType.ancillaries_legendary):
                self.waaaghMessenger.run("give_player_ancillary(\"%s\")" % (item.name))
            elif item.type == ItemType.effect_faction:
                self.waaaghMessenger.run("give_player_faction_effect(\"%s\")" % (item.name))
            elif item.type == ItemType.filler_strong:
                if item.name == "Give me that":
                    self.waaaghMessenger.run("force_settlement_transfer_from_random_enemy_to_player()")
                elif item.name == "Make Love, Not War":
                    self.waaaghMessenger.run("force_alliance_with_random_enemy()")
            elif item.type == ItemType.trap_harmless:
                if self.are_traps_enabled == True:
                    if item.name == "Look! What\'s that?":
                        self.waaaghMessenger.run("scroll_camera_to_random_region()")
                    if item.name == "Spoiler Alert!":
                        self.waaaghMessenger.run("play_random_movie()")
                else:
                    self.waaaghMessenger.run("out(\"Skiped a Trap\")")
            elif item.type == ItemType.trap_weak:
                if self.are_traps_enabled == True:
                    if item.name == "Handfull of Unrest":
                        self.waaaghMessenger.run("set_random_negative_public_order()")
                    elif item.name == "Unionize This!":
                        self.waaaghMessenger.run("force_random_weak_rebellion_for_player()")
                    elif item.name == "Where is our Map?":
                        self.waaaghMessenger.run("cm:reset_shroud()")
                    elif item.name == "Schizophrenia!":
                        self.waaaghMessenger.run("cm:cai_force_personality_change(\"All\")")
                else:
                    self.waaaghMessenger.run("out(\"Skiped a Trap\")")
            elif item.type == ItemType.trap_strong:
                if self.are_traps_enabled == True:
                    if item.name == "Torches and Pitchforks!":
                        self.waaaghMessenger.run("force_random_strong_rebellion_for_player()")
                    elif item.name == "Let\'s trade!":
                        self.waaaghMessenger.run("force_settlement_trade_with_random_enemy()")
                    elif item.name == "You too, Brutus?":
                        self.waaaghMessenger.run("force_war_with_random_ally()")
                else:
                    self.waaaghMessenger.run("out(\"Skiped a Trap\")")
            elif item.type == ItemType.ritual:
                self.waaaghMessenger.run("cm:unlock_ritual(cm:get_faction(\"%s\"), \"%s\", 0)" % (self.playerFaction, item.name))

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

    def send_next_progressive_tech(self, progressionGroup):
    # The Amount of progressive Items per Group is saved on the first index with that progression Group
        for id, item in self.item_table.items():
            if ((item.faction == self.playerFaction) and (item.progressionGroup == progressionGroup)):
                level_to_unlock = self.progressive_items_flags[id]
                self.progressive_items_flags[id] += 1
                break
        for id, item in self.item_table.items():
            if ((item.faction == self.playerFaction) and (item.progressionGroup == progressionGroup) and (item.tier == level_to_unlock)):
                self.waaaghMessenger.run("cm:unlock_technology(\"%s\", \"%s\")" % (self.playerFaction, item.name))

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
        try:
            await self.check_locations([self.locationLookup[location]])
        except ValueError as err:
            logger.error(err)
            logger.error("There is a Key Mismatch. Release location manually and please report the false Key to the discord server. Key is: " + location)

    # async def get_path(self):
    #     if not self.path:
    #         logger.info('Enter TWW3 Installation path:')
    #         self.path = await self.console_input()
    #         logger.info('Accepted Path is: ' + self.path)
    #         if not path or not os.path.exists(self.path):
    #             logger.error('Path does not point to a directory')
    #         if not os.path.isfile(self.path + '\\Warhammer3.exe'):
    #             logger.error('No TWW3 exe in Path')
    #         else:
    #             logger.info('Found TWW3 exe')

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
    def initialize(cls, context):
        settlements = context.settlements
        hordes = context.hordes
        randitem_list = context.randitemList
        playerFaction = context.playerFaction
        spheres = context.spheres
        capitals = context.capitals
        startingTier = context.startingTier
        waaaghMessenger = context.waaaghMessenger
        if (context.randomizePersonalities == True):
            waaaghMessenger.run("cm:cai_force_personality_change(\"All\")")
        for settlement, faction in settlements.items():
            waaaghMessenger.run("cm:transfer_region_to_faction(\"%s\", \"%s\")" % (settlement, faction))
            waaaghMessenger.run("cm:heal_garrison(cm:get_region(\"%s\"):cqi())" % (settlement))
        for faction, settlement in capitals.items():
            waaaghMessenger.run("teleport_all_heroes_of_faction_to_region(\"%s\", \"%s\")" % (faction, settlement))
            waaaghMessenger.run("teleport_all_lords_of_faction_to_region(\"%s\", \"%s\")" % (faction, settlement))
        for settlement, faction in hordes.items():
            waaaghMessenger.run("teleport_all_heroes_of_faction_to_region(\"%s\", \"%s\")" % (faction, settlement))
            waaaghMessenger.run("teleport_all_lords_of_faction_to_region(\"%s\", \"%s\")" % (faction, settlement))
        for itemNumber in randitem_list:
            itemData = context.item_table[itemNumber]
            if ((itemData.type == ItemType.tech) and (context.progressiveTechs == False) and (itemData.progressionGroup != None)):
                waaaghMessenger.run("cm:lock_one_technology_node(\"%s\", \"%s\")" % (playerFaction, itemData.name))
            elif ((itemData.type == ItemType.building) and (context.progressiveBuildings == False) and (itemData.progressionGroup != None)):
                waaaghMessenger.run("cm:add_event_restricted_building_record_for_faction(\"%s\", \"%s\")" % (itemData.name, playerFaction))
            elif ((itemData.type == ItemType.unit) and (context.progressiveUnits == False) and (itemData.progressionGroup != None)):
                waaaghMessenger.run("cm:add_event_restricted_unit_record_for_faction(\"%s\", \"%s\")" % (itemData.name, playerFaction))
        if (context.shuffleRituals == True):
            for key, ritual in ritual_table.items():
                if (ritual.faction == playerFaction):
                    waaaghMessenger.run("cm:lock_ritual(cm:get_faction(\"%s\"), \"%s\")" % (playerFaction, ritual.name))
        if (context.progressiveBuildings == True):
            cls.lock_progressive_buildings(playerFaction, startingTier, waaaghMessenger, context.item_table, context.progressive_items_flags)
        if (context.progressiveUnits == True):
            cls.lock_progressive_units(playerFaction, startingTier, waaaghMessenger, context.item_table, context.progressive_items_flags)
        if (context.progressiveTechs == True):
            cls.lock_progressive_techs(playerFaction, waaaghMessenger, context.item_table, context.progressive_items_flags)
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

    def lock_progressive_techs(playerFaction, waaaghMessenger, item_table, progressive_items_flags):
        for id, item in item_table.items():
            if ((item.faction == playerFaction) and (item.type == ItemType.tech) and (item.progressionGroup != None)):
                # The Amount of progressive Items per Group is saved on the first index with that progression Group, but since we don't know the first item of each progression Group, we set all items to the starting Tier for now.
                waaaghMessenger.run("cm:lock_one_technology_node(\"%s\", \"%s\")" % (playerFaction, item.name))

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