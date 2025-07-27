from .items import ItemType, ItemData
from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Dict, Set, List

filler_weak_table: Dict[int, ItemData] = {
    2000: ItemData(IC.filler, 0, "Get-Rich-Quick Scroll", ItemType.filler_weak, "None", None, "None"),
    2001: ItemData(IC.filler, 0, "Something Happened", ItemType.filler_weak, "None", None, "None"),
    2002: ItemData(IC.filler, 0, "Handfull of Order", ItemType.filler_weak, "None", None, "None"),
    2003: ItemData(IC.filler, 0, "Something Thingy", ItemType.filler_weak, "None", None, "None"),
    2005: ItemData(IC.filler, 0, "The GroBro 3000™", ItemType.filler_weak, "None", None, "None")
}

filler_strong_table: Dict[int, ItemData] = {
    2500: ItemData(IC.filler, 0, "Give me that", ItemType.filler_strong, "None", None, "None"),
    2501: ItemData(IC.filler, 0, "Make Love, Not War", ItemType.filler_strong, "None", None, "None"),
    2502: ItemData(IC.filler, 0, "Something Shiny", ItemType.filler_strong, "None", None, "None")
}

trap_harmless_table: Dict[int, ItemData] = {
    3000: ItemData(IC.trap, 0, "Look! What\'s that?", ItemType.trap_harmless, "None", None, "None"),
    3001: ItemData(IC.trap, 0, "Spoiler Alert!", ItemType.trap_harmless, "None", None, "None")
}

trap_weak_table: Dict[int, ItemData] = {
    3100: ItemData(IC.trap, 0, "Handfull of Unrest", ItemType.trap_weak, "None", None, "None"),
    3101: ItemData(IC.trap, 0, "Unionize This!", ItemType.trap_weak, "None", None, "None"),
    3104: ItemData(IC.trap, 0, "Where is our Map?", ItemType.trap_weak, "None", None, "None"),
    3105: ItemData(IC.trap, 0, "Schizophrenia!", ItemType.trap_weak, "None", None, "None")
}

trap_strong_table: Dict[int, ItemData] = {
    3200: ItemData(IC.trap, 0, "Torches and Pitchforks!", ItemType.trap_strong, "None", None, "None"),
    3205: ItemData(IC.trap, 0, "Let's trade!", ItemType.trap_strong, "None", None, "None"),
    3206: ItemData(IC.trap, 0, "You too, Brutus?", ItemType.trap_strong, "None", None, "None")
}