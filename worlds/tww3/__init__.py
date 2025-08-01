from typing import List, Dict, Any, cast, Mapping, ClassVar
from worlds.AutoWorld import World, WebWorld
from BaseClasses import Region, Location, Entrance, Item, ItemClassification
from .options import TWW3Options  # the options we defined earlier
from .item_tables.items import ItemType
from .item_tables.progression_table import progression_table
from .item_tables.filler_item_table import filler_weak_table, filler_strong_table, trap_harmless_table, trap_weak_table, trap_strong_table
from .item_tables.effect_table import global_effect_table
from .item_tables.ancillaries_table import ancillaries_regular_table, ancillaries_legendary_table
from .item_tables.unique_item_table import unique_item_table
from .item_tables.ritual_table import ritual_table
from .item_tables.progressive_buildings_table import progressive_buildings_table
from .item_tables.progressive_units_table import progressive_units_table
from .item_tables.progressive_techs_table import progressive_techs_table
from .filler_item_manager import Filler_Item_Manager
from .locations_table.locations import location_table, events  # same as above
from .locations_table.settlements import Settlement_Manager, lord_name_to_faction_dict
from .rules import set_rules
from worlds.generic.Rules import set_rule, add_rule
from worlds.LauncherComponents import components, Component, launch_subprocess, Type, icon_paths
from Utils import local_path
from BaseClasses import ItemClassification as IC
import os
import settings

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

class TWW3Settings(settings.Group):
    class TWW3Path(settings.FolderPath):
        """Installation Path to the TWW3 folder, so that input and output files can be written."""
        description = "Total War Warhammer 3 Installation Folder. Where the .exe is."

        # def validate(cls, path: str):
        #     if not path or not os.path.exists(path):
        #         raise ValueError('Path does not point to a directory')
        #     if not os.path.isfile(path + '\\Warhammer3.exe'):
        #         raise ValueError('No TWW3 exe in Path')


    tww3_path: TWW3Path = TWW3Path("C:/Program Files (x86)/Steam/steamapps/common/Total War WARHAMMER III")

class TWW3Location(Location):  # or from Locations import MyGameLocation
    game = "Total War Warhammer 3"  # name of the game/world this location is in

all_locations = {data["name"]: loc_id for loc_id, data in location_table.items()}

class TWW3World(World):
    """Insert description of the world/game here."""
    game = "Total War Warhammer 3"  # name of the game/world
    options_dataclass = TWW3Options  # options the player can set
    options: TWW3Options  # typing hints for option results
    settings: ClassVar[TWW3Settings]  # will be automatically assigned from type hint
    origin_region_name = "Old World"
    topology_present = False # show path to required location checks in spoiler
    item_table = dict(progression_table)
    item_table.update(filler_weak_table)
    item_table.update(filler_strong_table)
    item_table.update(global_effect_table)
    item_table.update(ancillaries_regular_table)
    item_table.update(ancillaries_legendary_table)
    item_table.update(trap_harmless_table)
    item_table.update(trap_weak_table)
    item_table.update(trap_strong_table)
    item_table.update(unique_item_table)
    item_table.update(progressive_buildings_table)
    item_table.update(progressive_units_table)
    item_table.update(progressive_techs_table)
    item_table.update(ritual_table)
    item_name_to_id = {data.name: item_id for item_id, data in item_table.items()}
    # print("Sinthoras Debug:")
    # print(len(item_name_to_id))
    # print(len(items.item_table.values()))
    # print(len(set(items.item_table.values())))
    location_name_to_id = all_locations
    location_amount = 0
    sm: Settlement_Manager = None
    factions_to_spheres = {}
    item_list = []

    # def get_filler_item_name(self) -> str:
    #     return "Gold"

    def generate_early(self):
        #self.player_faction = self.options.starting_faction.value
        self.player_faction = lord_name_to_faction_dict[self.options.starting_faction]
        self.sm: Settlement_Manager = Settlement_Manager(self.random)
        self.settlement_table, self.horde_table = self.sm.shuffle_settlements(self.player_faction, self.options.max_range) 

    def create_regions(self):
        # Create Region
        world_region = Region("Old World", self.player, self.multiworld)

        # Create regular locations
        location_names = (location["name"] for location in location_table.values())

        sphere_amount = self.options.spheres_option.value
        sphere_distance = self.options.sphere_distance.value
        self.factions_to_spheres = self.sm.factions_to_spheres(sphere_amount, sphere_distance)

        if self.options.balance_spheres == True:
            self.item_name_groups = {
                "Unlocks": set()
            }
            for item, value in self.item_table.items():
                if value.classification == IC.progression and value.faction == self.player_faction:
                    self.item_name_groups["Unlocks"].add(value.name)

            self.sm.get_settlement_spheres()
            sphere_amount = self.options.spheres_option.value
            settlements_per_sphere = self.sm.count_settlements_per_sphere(sphere_amount)
            unlock_percentage = self.options.balance_spheres_percentage
            items_per_sphere = {}
            for i in range(sphere_amount):
                required_items = int(settlements_per_sphere[i] * unlock_percentage/100)
                items_per_sphere[i] = required_items
            
            max_items = 0
            if self.options.building_shuffle:
                if self.options.progressive_buildings:
                    for value in set(progressive_buildings_table.values()):
                        if ((value.faction == self.player_faction) and (value.tier +1 > self.options.starting_tier.value)):
                            max_items += 1
                else:
                    for value in set(unique_item_table.values()):
                        if ((value.faction == self.player_faction) and (value.type == ItemType.building) and (value.tier +1 > self.options.starting_tier.value)):
                            max_items += 1
            if self.options.unit_shuffle:
                if self.options.progressive_units:
                    for value in set(progressive_units_table.values()):
                        if ((value.faction == self.player_faction) and (value.tier > self.options.starting_tier.value)):
                            max_items += 1
                else:
                    for value in set(unique_item_table.values()):
                        if ((value.faction == self.player_faction) and (value.type == ItemType.unit) and (value.tier > self.options.starting_tier.value)):
                            max_items += 1
            if self.options.tech_shuffle:
                if self.options.progressive_technologies:
                    for value in set(progressive_techs_table.values()):
                        if (value.faction == self.player_faction):
                            max_items += 1
                else:
                    for value in set(unique_item_table.values()):
                        if ((value.faction == self.player_faction) and (value.type == ItemType.tech)):
                            max_items += 1
            max_unlocks = self.options.balance_spheres_max_unlocks.value

        
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
                        if (self.options.balance_spheres == True) and (items_per_sphere[required_spheres - 1] != 0):
                            sum = 0
                            for i in range(0, required_spheres - 1):
                                sum += items_per_sphere[required_spheres - 1]
                            if (self.options.balance_spheres_max_unlocks.value != 0):
                                if (sum > max_unlocks):
                                    sum = max_unlocks
                            else:
                                if (sum > max_items):
                                    sum = max_items
                            add_rule(location, lambda state, new_sum=sum: state.has_group("Unlocks", self.player, new_sum))
                    elif ((required_spheres >= sphere_amount) and (self.options.sphere_world.value)):
                        set_rule(location, lambda state, spheres=sphere_amount: state.has("Sphere of Influence", self.player, spheres - 1))
                        if (self.options.balance_spheres == True) and (items_per_sphere[sphere_amount - 2] != 0):
                            sum = 0
                            for i in range(0, sphere_amount - 2):
                                sum += items_per_sphere[sphere_amount - 2]
                            if (self.options.balance_spheres_max_unlocks.value != 0):
                                if (sum > max_unlocks):
                                    sum = max_unlocks
                            else:
                                if (sum > max_items):
                                    sum = max_items
                            add_rule(location, lambda state, new_sum=sum: state.has_group("Unlocks", self.player, new_sum))
                    elif ((required_spheres >= sphere_amount) and (not self.options.sphere_world.value)):
                        continue
            world_region.locations.append(location)

       



        # Create events
        goal_event_name = self.options.goal.get_event_name()

        for event in events:
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
        self.location_amount = len(world_region.locations)

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
                    elif ((self.options.tech_shuffle.value == True) and (item.type == ItemType.tech) and (self.options.progressive_technologies == False)):
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

        if (self.options.progressive_technologies == True):
            for item_id, item in progressive_techs_table.items():
                if ((item.faction == self.player_faction) and (self.options.tech_shuffle.value == True)):
                    tww3_item = self.create_item(item.name)
                    pool.append(tww3_item)

        if (self.options.ritual_shuffle == True):
            for item_id, item in ritual_table.items():
                if (item.faction == self.player_faction):
                    tww3_item = self.create_item(item.name)
                    pool.append(tww3_item)

        for _ in range(self.options.domination_option.value):
            tww3_item = self.create_item("Orb of Domination")
            pool.append(tww3_item)

        for _ in range(self.options.spheres_option.value - 1):
            tww3_item = self.create_item("Sphere of Influence")
            pool.append(tww3_item)

        item_amount: int = len(pool)

        item_manager = Filler_Item_Manager(self.options.filler_weak.value, self.options.filler_strong.value, self.options.trap_harmless.value, self.options.trap_weak.value, self.options.trap_strong.value, self.random)
        for _ in range(self.location_amount - 1 - item_amount):
            #item = self.create_filler()
            #item = cast(TWW3Item, item)
            item_name = item_manager.roll_for_item()
            item = self.create_item(item_name)
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
        if self.options.tech_shuffle.value == True:
            slot_data["ProgressiveTechs"] = self.options.progressive_technologies.value
        else:
            slot_data["ProgressiveTechs"] = False
        if self.options.building_shuffle.value == True:
            slot_data["ProgressiveBuildings"] = self.options.progressive_buildings.value
        else:
            slot_data["ProgressiveBuildings"] = False
        if self.options.unit_shuffle.value == True:
            slot_data["ProgressiveUnits"] = self.options.progressive_units.value
        else:
            slot_data["ProgressiveUnits"] = False
        slot_data["StartingTier"] = self.options.starting_tier.value
        slot_data["DominationGoal"] = self.options.domination_option.value
        slot_data["RandomizePersonalities"] = self.options.RandomizePersonalities.value
        slot_data["Ritual_Shuffle"] = self.options.ritual_shuffle.value
        slot_data["Settlements"] = self.settlement_table
        slot_data["Hordes"] = self.horde_table
        slot_data["Spheres"] = self.factions_to_spheres
        slot_data["FactionCapitals"] = self.sm.get_capital_dict()
        slot_data["Items"] = self.item_list
        

        return slot_data

    def create_item(self, name: str) -> TWW3Item:
        item_id: int = self.item_name_to_id[name]

        return TWW3Item(name, self.item_table[item_id].classification, item_id, player=self.player)