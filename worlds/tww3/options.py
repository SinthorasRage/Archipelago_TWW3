from Options import Choice, DeathLink, DefaultOnToggle, Range, StartInventoryPool, PerGameCommonOptions, Toggle
from dataclasses import dataclass

class Faction(Choice):
    display_name = "Player Faction"
    option_KarlFranz = 1
    default = 1

class FactionShuffle(DefaultOnToggle):
    display_name = "FactionShuffle"

class TechShuffle(Toggle):
    display_name = "TechShuffle"

class BuildingShuffle(Toggle):
    display_name = "BuildingShuffle"

class ProgressiveBuildings(DefaultOnToggle):
    display_name = "Progressive Buildings"

class UnitShuffle(Toggle):
    display_name = "UnitShuffle"

class ProgressiveUnits(DefaultOnToggle):
    display_name = "Progressive Units"


class Spheres(Range):
    range_start = 1
    range_end = 65
    default = 7

class SphereDistance(Range):
    # Min Range between Settlements is 24. Max Range is 1300.
    range_start = 20
    range_end = 500
    default = 300

class SphereWorld(Toggle):
    display_name = "Should Settlements outside last Sphere be included in last Sphere"

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
    range_end = 100
    default = 20

@dataclass
class TWW3Options(PerGameCommonOptions):
    starting_faction: Faction
    faction_shuffle: FactionShuffle
    tech_shuffle: TechShuffle
    building_shuffle: BuildingShuffle
    progressive_buildings: ProgressiveBuildings
    unit_shuffle: UnitShuffle
    progressive_units: ProgressiveUnits
    spheres_option: Spheres
    sphere_distance: SphereDistance
    sphere_world: SphereWorld
    goal: Goal
    domination_option: Domination_Amount

