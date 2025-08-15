from Options import Choice, DeathLink, DefaultOnToggle, Range, StartInventoryPool, PerGameCommonOptions, Toggle
from dataclasses import dataclass

class Faction(Choice):
    """Choose your Player Faction. In case you pick multiple factions, the Client will tell you after connecting which one you play.
    Don't forget to remove the weight from the first entry."""
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
    default = 1

class FactionShuffle(DefaultOnToggle):
    """If you want to shuffle the settlements for each faction"""
    display_name = "FactionShuffle"

class MaxRange(Range):
    """How far away a Settlement can be from a factions other settlements.
    The minimal distance between two settlements is around 23 units, the maximum distance is about 1500 units"""
    range_start = 50
    range_end = 1500
    default = 200

class TechShuffle(DefaultOnToggle):
    """If Technologies should be shuffled."""
    display_name = "TechShuffle"

class ProgressiveTechnologies(DefaultOnToggle):
    """If Technologies should be progressive. Requires TechShuffle to be on."""
    display_name = "Progressive Technologies"

class BuildingShuffle(DefaultOnToggle):
    """If Buildings should be shuffled."""
    display_name = "BuildingShuffle"

class ProgressiveBuildings(DefaultOnToggle):
    """If Buildings should be progressive. Requires BuildingShuffle to be on."""
    display_name = "Progressive Buildings"

class UnitShuffle(DefaultOnToggle):
    """If Units should be shuffled."""
    display_name = "UnitShuffle"

class ProgressiveUnits(DefaultOnToggle):
    """If Units should be progressive. Requires UnitShuffle to be on."""
    display_name = "Progressive Units"

class RitualShuffle(Toggle):
    """Should Faction Mechanics like Rituals be shuffled? Will make game probably harder. Also experimental Feature."""
    display_name ="Shuffle Faction Mechanics like Rituals"

class StartingTier(Range):
    """Start with Buildings and Units with the specified Tier."""
    range_start = 0
    range_end = 5
    default = 1

class Spheres(Range):
    """How many diplomatic Spheres are required to goal. You can only engage in Diplomacy with factions that are in your sphere.
    Collect Spheres of Influence to expand your Sphere."""
    range_start = 1
    range_end = 65
    default = 7

class ExtraSpheres(Range):
    """How many extra diplomatic Spheres are in the game in addition to the ones required. Since there is at the moment a small chance to softlock, a few extra spheres should be chosen."""
    range_start = 1
    range_end = 50
    default = 5

class SphereDistance(Range):
    """Distance of each Sphere."""
    # Min Range between Settlements is 24. Max Range is 1300.
    range_start = 20
    range_end = 500
    default = 300

class SphereWorld(Toggle):
    """Should Settlements outside last Sphere be included in the last Sphere? 
    Can make the game considerably longer, since all Settlements will be in the game."""
    display_name = "Should Settlements outside last Sphere be included in last Sphere"

class BalanceSpheres(DefaultOnToggle):
    """Set's requirements for spheres so that Unit, Building and Tech Unlocks are pushed towards earlier spheres.
    Will make the unlocks appear smoother over the game instead of most of them at the end."""
    display_name = "Should Unlocks be requirements for the next sphere"

class BalanceSpheresPercentage(Range):
    """How many percantage of checks in per sphere needs to be at least unlocks."""
    range_start = 1
    range_end = 100
    default = 50

class BalanceSpheresMaxUnlocks(Range):
    """The maximum number of unlocks required for the last sphere.
    Was an option to workaround a bug, but the bug is fixed. Use it if you want, otherwise just let it disabled."""
    range_start = 0
    range_end = 200
    default = 0

class Goal(Choice):
    """Collect a number of Orb of Dominance Items to win your World."""
    auto_display_name = True
    display_name = "Goal"
    option_domination = 0

    def get_event_name(self) -> str:
        return {
            self.option_domination: "World Domination"
        }[self.value]

class Domination_Amount(Range):
    """How many Orb of Dominance Items are in your World."""
    range_start = 1
    range_end = 100
    default = 20

class ExtraDominationOrbs(Range):
    """How many extra Domination Orbs should be in the game in addition to the ones required."""
    range_start = 1
    range_end = 50
    default = 0

class filler_weak(Range):
    """Weight of weak filler items.
    Example: filler_weak: 30, filler_strong: 10, trap_harmless: 30, trap_weak: 25, trap_strong: 5
    Would mean, that approximatelly 30% are weak filler, 10% are strong filler, etc, since the weights add up to 100.
    You can deviate from that, but it will be less intuitive if the total number of weights is not 100."""
    range_start = 0
    range_end = 100
    default = 30

class filler_strong(Range):
    """Weight of strong filler items.
    Experimental Feature."""
    range_start = 0
    range_end = 100
    default = 10

class trap_harmless(Range):
    """Weight of harmless traps.
    Experimental Feature."""
    range_start = 0
    range_end = 100
    default = 30

class trap_weak(Range):
    """Weight of weak traps.
    Be careful, collecting a vast amount of them may require you to start a new save.
    Experimental Feature."""
    range_start = 0
    range_end = 100
    default = 20

class trap_strong(Range):
    """Weight of weak traps.
    Be careful, collecting a medium amount of them may require you to start a new save.
    Experimental Feature."""
    range_start = 0
    range_end = 100
    default = 10

class RandomizePersonalities(Toggle):
    """Randomize AI Personalities."""
    display_name = "Randomize Personality of each AI faction"

class NoMovieTraps(Toggle):
    """Replaces the movie traps to avoid sudden flashing lights. Experimental feature, but should hopefully work. Please report if it doesn't."""
    display_name = "Replaces the movie traps"

@dataclass
class TWW3Options(PerGameCommonOptions):
    starting_faction: Faction
    faction_shuffle: FactionShuffle
    max_range: MaxRange
    tech_shuffle: TechShuffle
    progressive_technologies: ProgressiveTechnologies
    building_shuffle: BuildingShuffle
    progressive_buildings: ProgressiveBuildings
    unit_shuffle: UnitShuffle
    progressive_units: ProgressiveUnits
    starting_tier: StartingTier
    spheres_option: Spheres
    extra_spheres: ExtraSpheres
    sphere_distance: SphereDistance
    sphere_world: SphereWorld
    balance_spheres: BalanceSpheres
    balance_spheres_percentage: BalanceSpheresPercentage
    balance_spheres_max_unlocks: BalanceSpheresMaxUnlocks
    goal: Goal
    domination_option: Domination_Amount
    extra_domination_orbs: ExtraDominationOrbs
    filler_weak: filler_weak
    filler_strong: filler_strong
    trap_harmless: trap_harmless
    trap_weak: trap_weak
    trap_strong: trap_strong
    RandomizePersonalities: RandomizePersonalities
    ritual_shuffle: RitualShuffle
    no_movie_trap: NoMovieTraps