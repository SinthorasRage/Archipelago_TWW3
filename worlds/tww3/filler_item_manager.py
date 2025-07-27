from .item_tables.items import ItemType, ItemData
from .item_tables.filler_item_table import filler_weak_table, filler_strong_table, trap_harmless_table, trap_weak_table, trap_strong_table
from .item_tables.effect_table import global_effect_table
from .item_tables.ancillaries_table import ancillaries_regular_table, ancillaries_legendary_table
from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Dict, Set, List

class Filler_Item_Manager:

    def __init__(self, filler_weak, filler_strong, trap_harmless, trap_weak, trap_strong, random):
        self.random = random
        self.filler_weak = filler_weak
        self.filler_strong = filler_strong
        self.trap_harmless = trap_harmless
        self.trap_weak = trap_weak
        self.trap_strong = trap_strong
        self.total = 0
        self.total = filler_weak + filler_strong + trap_harmless + trap_weak + trap_strong
        if (self.total == 0):
            raise Exception("Weigthing of Filler and Traps can't be 0")
        
    def roll_for_item(self):
        roll = self.random.randint(1, self.total)
        if roll <= self.filler_weak:
            return self.get_filler_weak()
        elif (roll > self.filler_weak) and (roll <= (self.filler_weak + self.filler_strong)):
            return self.get_filler_strong()
        elif (roll > (self.filler_weak + self.filler_strong)) and (roll <= (self.filler_weak + self.filler_strong + self.trap_harmless)):
            return self.get_trap_harmless()
        elif (roll > (self.filler_weak + self.filler_strong + self.trap_harmless)) and (roll <= (self.filler_weak + self.filler_strong + self.trap_harmless + self.trap_weak)):
            return self.get_trap_weak()
        elif (roll > (self.filler_weak + self.filler_strong + self.trap_harmless + self.trap_weak)) and (roll <= (self.filler_weak + self.filler_strong + self.trap_harmless + self.trap_weak + self.trap_strong)):
            return self.get_trap_strong()
        else:
            raise Exception("Roll in roll_for_item was higher than allowed.")
        
    def get_filler_weak(self):
        item_table = filler_weak_table
        key = self.random.choice(tuple(item_table.keys()))
        # apply random effect
        if key == 2001:
            effect_table = global_effect_table
            name = self.random.choice(tuple(effect_table.values())).name
            return name
        # get random ancillary
        elif key == 2003:
            ancillaries_table = ancillaries_regular_table
            name = self.random.choice(tuple(ancillaries_table.values())).name
            return name
        else:
            name = item_table[key].name
            return name
        
    def get_filler_strong(self):
        item_table = filler_strong_table
        key = self.random.choice(tuple(item_table.keys()))
        # get legendary ancillary
        if key == 2502:
            ancillaries_table = ancillaries_legendary_table
            name = self.random.choice(tuple(ancillaries_table.values())).name
            return name
        else:
            name = item_table[key].name
            return name
        
    def get_trap_harmless(self):
        item_table = trap_harmless_table
        key = self.random.choice(tuple(item_table.keys()))
        name = item_table[key].name
        return name
    
    def get_trap_weak(self):
        item_table = trap_weak_table
        key = self.random.choice(tuple(item_table.keys()))
        name = item_table[key].name
        return name

    def get_trap_strong(self):
        item_table = trap_strong_table
        key = self.random.choice(tuple(item_table.keys()))
        name = item_table[key].name
        return name
        