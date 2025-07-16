from Options import Choice, DeathLink, DefaultOnToggle, Range, StartInventoryPool, PerGameCommonOptions, Toggle
from dataclasses import dataclass

class Faction(Choice):
    display_name = "Player Faction"
    option_beastmen = 1
    option_morghur_herd = 2
    option_argwylon = 3
    option_wood_elves = 4
    option_norsca = 5
    option_wintertooth = 6
    option_bordeleaux = 7
    option_bretonnia = 8
    option_carcassonne = 9
    option_chaos = 10
    option_dwarfs = 11
    option_karak_izor = 12
    option_karak_kadrin = 13
    option_empire = 14
    option_wissenland = 15
    option_crooked_moon = 16
    option_greenskins = 17
    option_orcs_of_the_bloody_hand = 18
    option_schwartzhafen = 19
    option_vampire_counts = 20
    option_clan_rictus = 21
    option_exiles_of_nehek = 22
    option_followers_of_nagash = 23
    option_khemri = 24
    option_lybaras = 25
    option_noctilus = 26
    option_pirates_of_sartosa = 27
    option_the_drowned = 28
    option_vampire_coast = 29
    option_the_blessed_dread = 30
    option_the_barrow_legion = 31
    option_cult_of_sotek = 32
    option_golden_order = 33
    option_the_huntmarshals_expedition = 34
    option_spirits_of_the_jungle = 35
    option_chevaliers_de_lyonesse = 36
    option_bonerattlaz = 37
    option_broken_axe = 38
    option_imrik = 39
    option_drycha = 40
    option_sisters_of_twilight = 41
    option_malagor = 42
    option_taurox = 43
    option_thorek_ironbrow = 44
    option_oxyotl = 45
    option_cult_of_pleasure = 46
    option_hag_graef = 47
    option_har_ganeth = 48
    option_naggarond = 49
    option_avelorn = 50
    option_eataine = 51
    option_nagarythe = 52
    option_order_of_loremasters = 53
    option_yvresse = 54
    option_hexoatl = 55
    option_itza = 56
    option_last_defenders = 57
    option_tlaqua = 58
    option_clan_eshin = 59
    option_clan_mors = 60
    option_clan_moulder = 61
    option_clan_pestilens = 62
    option_clan_skryre = 63
    option_rakarth = 64
    option_azazel = 65
    option_festus = 66
    option_kholek = 67
    option_sigvald = 68
    option_valkia = 69
    option_vilitch = 70
    option_astragoth = 71
    option_legion_of_azgorh = 72
    option_zhatan = 73
    option_the_celestial_court = 74
    option_daughters_of_the_forest = 75
    option_the_deceivers = 76
    option_malakai = 77
    option_epidemius = 78
    option_tamurkhan = 79
    option_gorbad_ironclaw = 80
    option_arbaal = 81
    option_skulltaker = 82
    option_golgfag = 83
    option_shadow_legion = 84
    option_the_northern_provinces = 85
    option_the_western_provinces = 86
    option_daemon_prince = 87
    option_the_ancestral_throng = 88
    option_cult_of_sigmar = 89
    option_exiles_of_khorne = 90
    option_the_great_orthodoxy = 91
    option_the_ice_court = 92
    option_ursun_revivalists = 93
    option_poxmakers_of_nurgle = 94
    option_disciples_of_the_maw = 95
    option_goldtooth = 96
    option_seducers_of_slaanesh = 97
    option_oracles_of_tzeentch = 98
    option_caravan_of_blue_roses = 99
    default = 14

class FactionShuffle(DefaultOnToggle):
    display_name = "FactionShuffle"

class MaxRange(Range):
    # How far away a Settlement can be from a factions other settlements.
    range_start = 50
    range_end = 1500
    default = 200

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

class StartingTier(Range):
    # Min Range between Settlements is 24. Max Range is 1300.
    range_start = 0
    range_end = 5
    default = 1

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

class BalanceSpheres(Toggle):
    display_name = "Should Unlocks be requirements for the next sphere"

class BalanceSpheresPercentage(Range):
    # How many percantage of checks in per sphere needs to be at least unlocks.
    range_start = 1
    range_end = 100
    default = 50

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
    max_range: MaxRange
    tech_shuffle: TechShuffle
    building_shuffle: BuildingShuffle
    progressive_buildings: ProgressiveBuildings
    unit_shuffle: UnitShuffle
    progressive_units: ProgressiveUnits
    starting_tier: StartingTier
    spheres_option: Spheres
    sphere_distance: SphereDistance
    sphere_world: SphereWorld
    balance_spheres: BalanceSpheres
    balance_spheres_percentage: BalanceSpheresPercentage
    goal: Goal
    domination_option: Domination_Amount

