from Options import Choice, DeathLink, DefaultOnToggle, Range, StartInventoryPool, PerGameCommonOptions, Toggle
from dataclasses import dataclass

class Faction(Choice):
    display_name = "Player Faction"
    option_KarlFranz = 1
    default = 1

class FactionShuffle(Toggle):
    display_name = "FactionShuffle"

class TechShuffle(Toggle):
    display_name = "TechShuffle"

class UnitShuffle(Toggle):
    display_name = "UnitShuffle"

class Spheres(Range):
    range_start = 1
    range_end = 5
    default = 3

class Missions(Range):
    range_start = 1
    range_end = 300
    default = 300

class Goal(Choice):
    auto_display_name = True
    display_name = "Goal"
    option_domination = 0

    def get_event_name(self) -> str:
        return {
            self.option_domination: "World Domination"
        }[self.value]

class Domination_Amount(Range):
    range_start = 1
    range_end = 10
    default = 3

@dataclass
class TWW3Options(PerGameCommonOptions):
    starting_faction: Faction
    faction_shuffle: FactionShuffle
    tech_shuffle: TechShuffle
    unit_shuffle: UnitShuffle
    spheres_option: Spheres
    missions_option: Missions
    goal: Goal
    domination_option: Domination_Amount

