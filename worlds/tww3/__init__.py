from typing import List, Dict, Any, cast, Mapping
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Entrance, Item, ItemClassification
from .options import TWW3Options  # the options we defined earlier
from .item_tables.items import ItemType
from .item_tables.progression_filler_table import progression_table, filler_table
from .item_tables.unique_item_table import unique_item_table
from .item_tables.progressive_buildings_table import progressive_buildings_table
from .item_tables.progressive_units_table import progressive_units_table
from .locations import location_table  # same as above
from .settlements import Settlement_Manager, lord_name_to_faction_dict
from .rules import set_rules
from worlds.generic.Rules import set_rule
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths
from Utils import local_path

def launch_client():
    from .TWW3Client import launch
    launch_subprocess(launch, name="TWW3Client")

components.append(Component("TWW3 Client",
                            func=launch_client,
                            component_type=Type.CLIENT))

# components.append(Component("TWW3 Client",
#                             func=launch_client,
#                             component_type=Type.CLIENT,
#                             icon="orc"))

# icon_paths["orc"] = local_path("worlds", "tww3", "icons", "orc.png")

class TWW3Item(Item):  # or from Items import MyGameItem
    game = "Total War Warhammer 3"  # name of the game/world this item is from

# class TWW3Settings(settings.Group):
#     pass

class TWW3Location(Location):  # or from Locations import MyGameLocation
    game = "Total War Warhammer 3"  # name of the game/world this location is in

all_locations = {data["name"]: loc_id for loc_id, data in location_table.items()}

class TWW3World(World):
    """Insert description of the world/game here."""
    game = "Total War Warhammer 3"  # name of the game/world
    options_dataclass = TWW3Options  # options the player can set
    options: TWW3Options  # typing hints for option results
    # settings: ClassVar[TWW3Settings]  # will be automatically assigned from type hint
    origin_region_name = "Old World"
    topology_present = False # show path to required location checks in spoiler
    item_table = dict(progression_table)
    item_table.update(filler_table)
    item_table.update(unique_item_table)
    item_table.update(progressive_buildings_table)
    item_table.update(progressive_units_table)
    item_name_to_id = {data.name: item_id for item_id, data in item_table.items()}
    # print("Sinthoras Debug:")
    # print(len(item_name_to_id))
    # print(len(items.item_table.values()))
    # print(len(set(items.item_table.values())))
    location_name_to_id = all_locations
    sm: Settlement_Manager = None
    factions_to_spheres = {}
    item_list = []

    def get_filler_item_name(self) -> str:
        return "Gold"

    def generate_early(self):
        #self.player_faction = self.options.starting_faction.value
        self.player_faction = lord_name_to_faction_dict[self.options.starting_faction]
        self.sm: Settlement_Manager = Settlement_Manager(self.random)
        self.settlement_table, self.horde_table = self.sm.shuffle_settlements(self.player_faction) 

    def create_regions(self):
        # Create Region
        world_region = Region("Old World", self.player, self.multiworld)

        # Create regular locations
        location_names = (location["name"] for location in location_table.values())

        sphere_amount = self.options.spheres_option.value
        sphere_distance = self.options.sphere_distance.value
        self.factions_to_spheres = self.sm.factions_to_spheres(sphere_amount, sphere_distance)
        for location_name in location_names:
            loc_id = self.location_name_to_id[location_name]
            location = TWW3Location(self.player, location_name, loc_id, world_region)
            if location.address != None:
                faction: str = self.sm.settlement_to_faction(location.name)
                distance: int = self.sm.get_distance(faction)
                required_spheres = int(distance/sphere_distance)
                if (not (faction == lord_name_to_faction_dict[self.options.starting_faction])):
                    if ((required_spheres != 0) and (required_spheres < sphere_amount)):
                        set_rule(location, lambda state, spheres=required_spheres: state.has("Sphere of Influence", self.player, spheres))
                    elif ((required_spheres >= sphere_amount) and (self.options.sphere_world.value)):
                        set_rule(location, lambda state, spheres=required_spheres: state.has("Sphere of Influence", self.player, spheres - 1))
                    elif ((required_spheres >= sphere_amount) and (not self.options.sphere_world.value)):
                        continue
            world_region.locations.append(location)

        # Create events
        goal_event_name = self.options.goal.get_event_name()

        for event in locations.events:
            location = TWW3Location(self.player, event, None, world_region)
            world_region.locations.append(location)
            location.place_locked_item(
                TWW3Item(event, ItemClassification.progression, None, player=self.player)
                )
            if event == goal_event_name:
                # make the goal event the victory "item"
                location.item.name = "Victory"

        # Register region to multiworld
        self.multiworld.regions.append(world_region)

    # refer to rules.py
    
    set_rules = set_rules

    def create_items(self):
        # Generate item pool
        pool: List[TWW3Item] = []

        for item_id, item in unique_item_table.items():
            if (item.faction == self.player_faction):
                if (item.tier != None):
                    if ((item.tier > self.options.starting_tier.value) and (item.type == ItemType.unit) and (self.options.unit_shuffle.value == True) and (self.options.progressive_units == False)):
                        for i in range(item.count):
                            tww3_item = self.create_item(item.name)
                            pool.append(tww3_item)
                            self.item_list.append(item_id)
                    elif ((item.tier +1 > self.options.starting_tier.value) and (item.type == ItemType.building) and (self.options.building_shuffle.value == True) and (self.options.progressive_buildings == False)):
                        for i in range(item.count):
                            tww3_item = self.create_item(item.name)
                            pool.append(tww3_item)
                            self.item_list.append(item_id)
                elif ((self.options.tech_shuffle.value == True) and (item.type == ItemType.tech)):
                    for i in range(item.count):
                        tww3_item = self.create_item(item.name)
                        pool.append(tww3_item)
                        self.item_list.append(item_id)

        if (self.options.progressive_units == True):
            for item_id, item in progressive_units_table.items():
                if ((item.faction == self.player_faction) and (item.tier > self.options.starting_tier.value) and (self.options.unit_shuffle.value == True)):
                    tww3_item = self.create_item(item.name)
                    pool.append(tww3_item)

        if (self.options.progressive_buildings == True):
            for item_id, item in progressive_buildings_table.items():
                if ((item.faction == self.player_faction) and (item.tier +1 > self.options.starting_tier.value) and (self.options.building_shuffle.value == True)):
                    tww3_item = self.create_item(item.name)
                    pool.append(tww3_item)

        for _ in range(self.options.domination_option.value):
            tww3_item = self.create_item("Orb of Domination")
            pool.append(tww3_item)

        for _ in range(self.options.spheres_option.value - 1):
            tww3_item = self.create_item("Sphere of Influence")
            pool.append(tww3_item)

        item_amount: int = len(pool)
        location_amount: int = len(all_locations)

        for _ in range(location_amount - item_amount):
            item = self.create_filler()
            item = cast(TWW3Item, item)
            pool.append(item)

        self.multiworld.itempool += pool

    def fill_slot_data(self) -> Mapping[str, Any]:
        """
        Return the `slot_data` field that will be in the `Connected` network package.

        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response.

        :return: A dictionary to be sent to the client when it connects to the server.
        """
        slot_data: Dict = {}
        
        slot_data["PlayerFaction"] = self.options.starting_faction.value
        slot_data["ProgressiveBuildings"] = self.options.progressive_buildings.value
        slot_data["ProgressiveUnits"] = self.options.progressive_units.value
        slot_data["StartingTier"] = self.options.starting_tier.value
        slot_data["DominationGoal"] = self.options.domination_option.value
        slot_data["Settlements"] = self.settlement_table
        slot_data["Hordes"] = self.horde_table
        slot_data["Spheres"] = self.factions_to_spheres
        slot_data["FactionCapitals"] = self.sm.get_capital_dict()
        slot_data["Items"] = self.item_list
        

        return slot_data

    def create_item(self, name: str) -> TWW3Item:
        item_id: int = self.item_name_to_id[name]

        return TWW3Item(name, self.item_table[item_id].classification, item_id, player=self.player)