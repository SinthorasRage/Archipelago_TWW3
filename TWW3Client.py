from CommonClient import CommonContext, ClientCommandProcessor, server_loop, get_base_parser, logger
import Utils
import asyncio
import colorama
import logging
import copy
from worlds.tww3.items import item_table, ItemType
from worlds.tww3.locations import location_table
import io

class TWW3CommandProcessor(ClientCommandProcessor):
    pass

class TWW3Context(CommonContext):
    command_processor = TWW3CommandProcessor
    items_handling = 0b111

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.initialized = False
        self.waaaghMessenger = WaaaghMessenger('tmp.in')
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
        self.player_faction = 'wh_main_emp_empire'
        EngineInitializer.initialize(self.settlements, self.waaaghMessenger)

    def on_received_items(self, args: dict):
        numberOfGoalItems = 0
        for entry in self.items_received:
            item = item_table[entry.item]
            if item.type == ItemType.building:
                self.waaaghMessenger.run("cm:remove_event_restricted_building_record_for_faction(%s, %s)" % (item.name, self.player_faction))
            elif item.type == ItemType.technology:
                self.waaaghMessenger.run("cm:unlock_technology(%s, %s)" % (self.player_faction, item.name))
            elif item.type == ItemType.unit:
                self.waaaghMessenger.run("cm:remove_event_restricted_unit_record_for_faction(%s, %s)" % (item.name, self.player_faction))
            elif item.type == ItemType.goal:
                numberOfGoalItems = numberOfGoalItems + 1
        if numberOfGoalItems == 3:
            asyncio.create_task(self.send_msgs([{"cmd": "StatusUpdate", "status": 30}]))
        self.waaaghMessenger.flush()

    def on_print_json(self, args: dict):
        pass #print(args)

    async def check(self, location):
        await self.check_locations([self.locationLookup[location]])

class EngineInitializer():
    @classmethod
    def initialize(cls, settlements, waaaghMessenger):
        for entry in settlements.values():
            waaaghMessenger.run("cm:transfer_region_to_faction(%s, %s)" % (entry['settlement'], entry['faction']))        
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

        waaaghWatcher = WaaaghWatcher('tmp.out', ctx)
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