from .items import ItemType, ItemData
from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Dict, Set, List

progression_table: Dict[int, ItemData] = {
   1000: ItemData(IC.progression, 0, "Orb of Domination", ItemType.goal, "None", None, None),
   1100: ItemData(IC.progression, 0, "Sphere of Influence", ItemType.progression, "None", None, None)
}

filler_table: Dict[int, ItemData] = {
    2000: ItemData(IC.filler, 0, "Gold", ItemType.filler, "None", None, None)
}