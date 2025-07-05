from CommonClient import CommonContext, ClientCommandProcessor, server_loop, get_base_parser, logger
import Utils
import asyncio
import colorama
import logging
import copy
from worlds.tww3.settlements import lord_name_to_faction_dict
from worlds.tww3.items import item_table, ItemType
from worlds.tww3.locations import location_table
import io

path = "I:\SteamLibrary\steamapps\common\Total War WARHAMMER III"

class TWW3CommandProcessor(ClientCommandProcessor):
    pass

class TWW3Context(CommonContext):
    command_processor = TWW3CommandProcessor
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.initialized = False
        self.waaaghMessenger = WaaaghMessenger(path + '\engine.in')
        self.game = 'Total War Warhammer 3'

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TWW3Context, self).server_auth(password_requested)
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.on_connected(args)
        elif cmd == "ReceivedItems":
            self.on_received_items(args)

    def on_connected(self, args: dict):
        self.settlements = args['slot_data']['Settlements']
        self.locationLookup = dict()
        for key, entry in location_table.items():
            self.locationLookup[entry['name']] = int(key)
        self.playerFaction = lord_name_to_faction_dict[args['slot_data']['PlayerFaction']]
        self.randitemList = args['slot_data']['Items']
        self.goalNumber = args['slot_data']['DominationGoal']
        self.spheres = args['slot_data']['Spheres']
        EngineInitializer.initialize(self.settlements, self.randitemList, self.playerFaction, self.spheres, self.waaaghMessenger)

    def on_received_items(self, args: dict):
        numberOfGoalItems = 0
        numberOfSphereItems = 0
        for entry in self.items_received:
            item = item_table[entry.item]
            if item.type == ItemType.building:
                self.waaaghMessenger.run("cm:remove_event_restricted_building_record_for_faction(\"%s\", \"%s\")" % (item.name, self.playerFaction))
            elif item.type == ItemType.technology:
                self.waaaghMessenger.run("cm:unlock_technology(\"%s\", \"%s\")" % (self.playerFaction, item.name))
            elif item.type == ItemType.unit:
                self.waaaghMessenger.run("cm:remove_event_restricted_unit_record_for_faction(\"%s\", \"%s\")" % (item.name, self.playerFaction))
            elif item.type == ItemType.goal:
                numberOfGoalItems = numberOfGoalItems + 1
            elif item.type == ItemType.progression:
                numberOfSphereItems = numberOfSphereItems + 1
                self.triggerProgressionEvents(numberOfSphereItems)
        if numberOfGoalItems == self.goalNumber:
            asyncio.create_task(self.send_msgs([{"cmd": "StatusUpdate", "status": 30}]))
        self.waaaghMessenger.flush()

    def triggerProgressionEvents(self, numberOfSphereItems):
        oldSphere = ()
        newSphere = ()
        allOthers = ()
        for faction, sphere in self.spheres.items():
            if sphere < numberOfSphereItems:
                oldSphere.append(faction)
            elif sphere == numberOfSphereItems:
                newSphere.append(faction)
            else:
                allOthers.append(faction)
        for oldFaction in oldSphere:
            for newFaction in newSphere:
                self.waaaghMessenger.run("cm:force_diplomacy(\"faction:%s\", \"faction:%s\", all, true, true, true)" % (oldFaction, newFaction))
        for newFaction in newSphere:
            for otherFaction in allOthers:
                self.waaaghMessenger.run("cm:force_make_peace(\"%s\", \"%s\")" % (newFaction, otherFaction))
                self.waaaghMessenger.run("cm:force_diplomacy(\"faction:%s\", \"faction:%s\", all, false, false, true)" % (newFaction, otherFaction))
        return

    def on_print_json(self, args: dict):
        pass #print(args)

    async def check(self, location):
        await self.check_locations([self.locationLookup[location]])

class EngineInitializer():
    @classmethod
    def initialize(cls, settlements, randitem_list, playerFaction, spheres, waaaghMessenger):
        for settlement, faction in settlements.items():
            waaaghMessenger.run("cm:transfer_region_to_faction(\"%s\", \"%s\")" % (settlement, faction))
            waaaghMessenger.run("teleport_all_heroes_of_faction_to_region(\"%s\", \"%s\")" % (faction, settlement))
            waaaghMessenger.run("teleport_all_lords_of_faction_to_region(\"%s\", \"%s\")" % (faction, settlement))
        for itemNumber in randitem_list:
            itemData = item_table[itemNumber]
            if itemData.type == ItemType.technology:
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
            await self.context.check(line.strip())

if __name__ == '__main__':
    Utils.init_logging('TWW3Client')
    logging.getLogger().setLevel(logging.INFO)

    async def main(args):
        ctx = TWW3Context(args.connect, args.password)
        ctx.auth = args.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name='ServerLoop')

        waaaghWatcher = WaaaghWatcher(path + '\engine.out', ctx)
        waaaghWatcher_task = asyncio.create_task(waaaghWatcher.watch(), name='WaaaghWatcher')
        
        await ctx.exit_event.wait()
        ctx.server_address = None
        await ctx.shutdown()

    parser = get_base_parser()
    parser.add_argument('--name', default=None, help='Slot Name to connect as.')
    args = parser.parse_args()
    colorama.just_fix_windows_console()

    asyncio.run(main(args))
    colorama.deinit()