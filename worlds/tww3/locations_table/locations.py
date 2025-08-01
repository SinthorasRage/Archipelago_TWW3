from typing import TypedDict, Dict, List
from .settlements import Settlement_Manager
import random

mission_types_table = [
    "ACHIVE_CHARACTER_RANK",
    "AMBUSH_ARMY",
    "ASSASSINATE_CHARACTER",
    "CAPTURE_REGIONS",
    "CAPTURE_X_BATTLE_CAPTIVES",
    "CONFEDERATE_FACTIONS",
    "CONSTRUCT_N_BUILDINGS_INCLUDING",
    "CONSTRUCT_N_OF_A_BUILDING",
    "DECLARE_WAR",
    "DEFEAT_N_ARMIES_OF_FACTION",
    "DEFEAT_ROGUE_ARMY",
    "EARN_X_AMOUNT_FROM_RAIDING",
    "ELIMINATE_CHARACTER_IN_BATTLE",
    "EMBED_AGENT",
    "ENGAGE_FORCE",
    "ENSURE_FACTIONS_HAVE_NO_MILITARY_PRESENCE",
    "FIGHT_SET_PIECE_BATTLE",
    "HAVE_AT_LEAST_X_MONEY",
    "HAVE_AT_LEAST_X_OF_A_POOLED_RESOURCE",
    "HAVE_CHARACTER_WITHIN_RANGE_OF_POSITION",
    "HAVE_RESOURCES",
    "HINDER_SETTLEMENT",
    "INCOME_AT_LEAST_X",
    "ISSUE_PROVINCE_INITIATIVE",
    "KILL_X_ENTITIES",
    "KILL_X_ENTITIES_BY",
    "MAKE_ALLIANCE",
    "MAKE_TRADE_AGREEMENT",
    "MOVE_TO_PROVINCE",
    "MOVE_TO_REGION",
    "MOVE_X_AGENTS_TO_Y_REGIONS_OWNED_BY_Z",
    "OCCUPY_LOOT_RAZE_OR_SACK_X_SETTLEMENTS",
    "OWN_N_PROVINCES",
    "OWN_N_UNITS",
    "PERFORM_ANY_AGENT_ACTION",
    "PERFORM_RITUAL",
    "RAID_REGION",
    "RAID_SUB_CULTURE",
    "RAISE_FORCE",
    "RAZE_OR_SACK_N_DIFFERENT_SETTLEMENTS_INCLUDING",
    "RAZE_OR_SACK_N_DIFFERENT_SETTLEMENTS_OF_SUBCULTURE",
    "RECRUIT_AGENT",
    "RECRUIT_N_UNITS_FROM",
    "RECRUIT_UNIT",
    "RESEARCH_TECHNOLOGY",
    "SEARCH_RUINS",
    "SIGN_NON_AGGRESSION_PACT"
]

events: List[str] = [
     "World Domination"
]

class LocationDict(TypedDict, total=False):
        name: str

location_table: Dict[int, LocationDict] = {
    1: {'name': 'wh3_main_combi_region_zlatlan'},
    2: {'name': 'wh3_main_combi_region_floating_village'},
    3: {'name': 'wh3_main_combi_region_shrine_of_khaine'},
    4: {'name': 'wh3_main_combi_region_mordheim'},
    5: {'name': 'wh3_main_combi_region_zoishenk'},
    6: {'name': 'wh3_main_combi_region_black_pyramid_of_nagash'},
    7: {'name': 'wh3_main_combi_region_hanyu_port'},
    8: {'name': 'wh3_main_combi_region_tor_yvresse'},
    9: {'name': 'wh3_main_combi_region_aquitaine'},
    10: {'name': 'wh3_main_combi_region_the_monolith_of_katam'},
    11: {'name': 'wh3_main_combi_region_helmgart'},
    12: {'name': 'wh3_main_combi_region_beichai'},
    13: {'name': 'wh3_main_combi_region_lashiek'},
    14: {'name': 'wh3_main_combi_region_steingart'},
    15: {'name': 'wh3_main_combi_region_floating_mountain'},
    16: {'name': 'wh3_main_combi_region_shrine_of_ladrielle'},
    17: {'name': 'wh3_main_combi_region_quatar'},
    18: {'name': 'wh3_main_combi_region_ancient_city_of_quintex'},
    19: {'name': 'wh3_main_combi_region_southern_outpost'},
    20: {'name': 'wh3_main_combi_region_black_iron_mine'},
    21: {'name': 'wh3_main_combi_region_vulture_mountain'},
    22: {'name': 'wh3_main_combi_region_dragons_crossroad'},
    23: {'name': 'wh3_main_combi_region_niedling'},
    24: {'name': 'wh3_main_combi_region_bleak_hold_fortress'},
    25: {'name': 'wh3_main_combi_region_dargoth'},
    26: {'name': 'wh3_main_combi_region_nagenhof'},
    27: {'name': 'wh3_main_combi_region_the_copper_landing'},
    28: {'name': 'wh3_main_combi_region_tor_surpindar'},
    29: {'name': 'wh3_main_combi_region_pools_of_despair'},
    30: {'name': 'wh3_main_combi_region_karak_angazhar'},
    31: {'name': 'wh3_main_combi_region_the_black_pillar'},
    32: {'name': 'wh3_main_combi_region_temple_avenue_of_gold'},
    33: {'name': 'wh3_main_combi_region_massif_orcal'},
    34: {'name': 'wh3_main_combi_region_white_tower_of_hoeth'},
    35: {'name': 'wh3_main_combi_region_winter_pyre'},
    36: {'name': 'wh3_main_combi_region_swamp_town'},
    37: {'name': 'wh3_main_combi_region_kemperbad'},
    38: {'name': 'wh3_main_combi_region_shrine_of_loec'},
    39: {'name': 'wh3_main_combi_region_karak_eight_peaks'},
    40: {'name': 'wh3_main_combi_region_the_palace_of_ruin'},
    41: {'name': 'wh3_main_combi_region_barag_dawazbag'},
    42: {'name': 'wh3_main_combi_region_nahuontl'},
    43: {'name': 'wh3_main_combi_region_deff_gorge'},
    44: {'name': 'wh3_main_combi_region_wei_jin'},
    45: {'name': 'wh3_main_combi_region_griffon_gate'},
    46: {'name': 'wh3_main_combi_region_shattered_cove'},
    47: {'name': 'wh3_main_combi_region_wurtbad'},
    48: {'name': 'wh3_main_combi_region_shard_bastion'},
    49: {'name': 'wh3_main_combi_region_isle_of_wights'},
    50: {'name': 'wh3_main_combi_region_ghrond'},
    51: {'name': 'wh3_main_combi_region_skavenblight'},
    52: {'name': 'wh3_main_combi_region_caverns_of_sotek'},
    53: {'name': 'wh3_main_combi_region_oakenhammer'},
    54: {'name': 'wh3_main_combi_region_tor_dranil'},
    55: {'name': 'wh3_main_combi_region_the_black_forests'},
    56: {'name': 'wh3_main_combi_region_stormvrack_mount'},
    57: {'name': 'wh3_main_combi_region_terracotta_graveyard'},
    58: {'name': 'wh3_main_combi_region_the_awakening'},
    59: {'name': 'wh3_main_combi_region_palace_of_princes'},
    60: {'name': 'wh3_main_combi_region_xahutec'},
    61: {'name': 'wh3_main_combi_region_the_writhing_fortress'},
    62: {'name': 'wh3_main_combi_region_elisia'},
    63: {'name': 'wh3_main_combi_region_mount_silverspear'},
    64: {'name': 'wh3_main_combi_region_wellsprings_of_eternity'},
    65: {'name': 'wh3_main_combi_region_tower_of_gorgoth'},
    66: {'name': 'wh3_main_combi_region_sarl_encampment'},
    67: {'name': 'wh3_main_combi_region_fort_jakova'},
    68: {'name': 'wh3_main_combi_region_miragliano'},
    69: {'name': 'wh3_main_combi_region_nuja'},
    70: {'name': 'wh3_main_combi_region_longship_graveyard'},
    71: {'name': 'wh3_main_combi_region_macu_peaks'},
    72: {'name': 'wh3_main_combi_region_norden'},
    73: {'name': 'wh3_main_combi_region_altar_of_spawns'},
    74: {'name': 'wh3_main_combi_region_tribeslaughter'},
    75: {'name': 'wh3_main_combi_region_sump_pit'},
    76: {'name': 'wh3_main_combi_region_grenzstadt'},
    77: {'name': 'wh3_main_combi_region_the_dust_gate'},
    78: {'name': 'wh3_main_combi_region_kappelburg'},
    79: {'name': 'wh3_main_combi_region_nan_gau'},
    80: {'name': 'wh3_main_combi_region_numas'},
    81: {'name': 'wh3_main_combi_region_lyonesse'},
    82: {'name': 'wh3_main_combi_region_lybaras'},
    83: {'name': 'wh3_main_combi_region_the_bleeding_spire'},
    84: {'name': 'wh3_main_combi_region_copher'},
    85: {'name': 'wh3_main_combi_region_nagashizzar'},
    86: {'name': 'wh3_main_combi_region_sunken_khernarch'},
    87: {'name': 'wh3_main_combi_region_mangrove_coast'},
    88: {'name': 'wh3_main_combi_region_grimtop'},
    89: {'name': 'wh3_main_combi_region_the_moon_shard'},
    90: {'name': 'wh3_main_combi_region_flayed_rock'},
    91: {'name': 'wh3_main_combi_region_eldar_spire'},
    92: {'name': 'wh3_main_combi_region_city_of_the_shugengan'},
    93: {'name': 'wh3_main_combi_region_laurelorn_forest'},
    94: {'name': 'wh3_main_combi_region_monument_of_izzatal'},
    95: {'name': 'wh3_main_combi_region_karaz_a_karak'},
    96: {'name': 'wh3_main_combi_region_dread_rock'},
    97: {'name': 'wh3_main_combi_region_village_of_the_moon'},
    98: {'name': 'wh3_main_combi_region_fu_hung'},
    99: {'name': 'wh3_main_combi_region_great_desert_of_araby'},
    100: {'name': 'wh3_main_combi_region_tlaqua'},
    101: {'name': 'wh3_main_combi_region_skrap_towers'},
    102: {'name': 'wh3_main_combi_region_fort_oberstyre'},
    103: {'name': 'wh3_main_combi_region_troll_fjord'},
    104: {'name': 'wh3_main_combi_region_rackdo_gorge'},
    105: {'name': 'wh3_main_combi_region_zandri'},
    106: {'name': 'wh3_main_combi_region_zanbaijin'},
    107: {'name': 'wh3_main_combi_region_kunlan'},
    108: {'name': 'wh3_main_combi_region_monolith_of_borkill_the_bloody_handed'},
    109: {'name': 'wh3_main_combi_region_venom_glade'},
    110: {'name': 'wh3_main_combi_region_xhotl'},
    111: {'name': 'wh3_main_combi_region_lost_plateau'},
    112: {'name': 'wh3_main_combi_region_elessaeli'},
    113: {'name': 'wh3_main_combi_region_spitepeak'},
    114: {'name': 'wh3_main_combi_region_the_gallows_tree'},
    115: {'name': 'wh3_main_combi_region_castle_carcassonne'},
    116: {'name': 'wh3_main_combi_region_shrine_of_sotek'},
    117: {'name': 'wh3_main_combi_region_tower_of_the_sun'},
    118: {'name': 'wh3_main_combi_region_fateweavers_crevasse'},
    119: {'name': 'wh3_main_combi_region_the_godless_crater'},
    120: {'name': 'wh3_main_combi_region_stonemine_tower'},
    121: {'name': 'wh3_main_combi_region_zavastra'},
    122: {'name': 'wh3_main_combi_region_rothkar_spire'},
    123: {'name': 'wh3_main_combi_region_the_daemons_stump'},
    124: {'name': 'wh3_main_combi_region_xen_wu'},
    125: {'name': 'wh3_main_combi_region_shagrath'},
    126: {'name': 'wh3_main_combi_region_clarak_spire'},
    127: {'name': 'wh3_main_combi_region_martek'},
    128: {'name': 'wh3_main_combi_region_ka_sabar'},
    129: {'name': 'wh3_main_combi_region_gateway_to_khuresh'},
    130: {'name': 'wh3_main_combi_region_cairn_thel'},
    131: {'name': 'wh3_main_combi_region_the_folly_of_malofex'},
    132: {'name': 'wh3_main_combi_region_karond_kar'},
    133: {'name': 'wh3_main_combi_region_dok_karaz'},
    134: {'name': 'wh3_main_combi_region_argalis'},
    135: {'name': 'wh3_main_combi_region_storag_kor'},
    136: {'name': 'wh3_main_combi_region_middenheim'},
    137: {'name': 'wh3_main_combi_region_languille'},
    138: {'name': 'wh3_main_combi_region_karak_azorn'},
    139: {'name': 'wh3_main_combi_region_black_tower_of_arkhan'},
    140: {'name': 'wh3_main_combi_region_pillar_of_skulls'},
    141: {'name': 'wh3_main_combi_region_desolation_of_nagash'},
    142: {'name': 'wh3_main_combi_region_blackstone_post'},
    143: {'name': 'wh3_main_combi_region_the_fortress_of_vorag'},
    144: {'name': 'wh3_main_combi_region_gor_gazan'},
    145: {'name': 'wh3_main_combi_region_pillars_of_unseen_constellations'},
    146: {'name': 'wh3_main_combi_region_marks_of_the_old_ones'},
    147: {'name': 'wh3_main_combi_region_karak_hirn'},
    148: {'name': 'wh3_main_combi_region_karak_raziak'},
    149: {'name': 'wh3_main_combi_region_zhufbar'},
    150: {'name': 'wh3_main_combi_region_karak_izor'},
    151: {'name': 'wh3_main_combi_region_tai_tzu'},
    152: {'name': 'wh3_main_combi_region_wolfenburg'},
    153: {'name': 'wh3_main_combi_region_weng_chang'},
    154: {'name': 'wh3_main_combi_region_hergig'},
    155: {'name': 'wh3_main_combi_region_fallen_gates'},
    156: {'name': 'wh3_main_combi_region_tobaro'},
    157: {'name': 'wh3_main_combi_region_qiang'},
    158: {'name': 'wh3_main_combi_region_cuexotl'},
    159: {'name': 'wh3_main_combi_region_great_skull_lakes'},
    160: {'name': 'wh3_main_combi_region_swartzhafen'},
    161: {'name': 'wh3_main_combi_region_eye_of_the_panther'},
    162: {'name': 'wh3_main_combi_region_fortress_of_the_damned'},
    163: {'name': 'wh3_main_combi_region_yuatek'},
    164: {'name': 'wh3_main_combi_region_the_blood_swamps'},
    165: {'name': 'wh3_main_combi_region_red_fortress'},
    166: {'name': 'wh3_main_combi_region_desolation_of_drakenmoor'},
    167: {'name': 'wh3_main_combi_region_tor_finu'},
    168: {'name': 'wh3_main_combi_region_grimhold'},
    169: {'name': 'wh3_main_combi_region_the_galleons_graveyard'},
    170: {'name': 'wh3_main_combi_region_sartosa'},
    171: {'name': 'wh3_main_combi_region_hag_hall'},
    172: {'name': 'wh3_main_combi_region_montfort'},
    173: {'name': 'wh3_main_combi_region_essen'},
    174: {'name': 'wh3_main_combi_region_fort_soll'},
    175: {'name': 'wh3_main_combi_region_bechafen'},
    176: {'name': 'wh3_main_combi_region_krugenheim'},
    177: {'name': 'wh3_main_combi_region_mahrak'},
    178: {'name': 'wh3_main_combi_region_daemons_gate'},
    179: {'name': 'wh3_main_combi_region_mine_of_the_bearded_skulls'},
    180: {'name': 'wh3_main_combi_region_tor_koruali'},
    181: {'name': 'wh3_main_combi_region_hell_pit'},
    182: {'name': 'wh3_main_combi_region_mighdal_vongalbarak'},
    183: {'name': 'wh3_main_combi_region_fortress_of_eyes'},
    184: {'name': 'wh3_main_combi_region_mousillon'},
    185: {'name': 'wh3_main_combi_region_mistnar'},
    186: {'name': 'wh3_main_combi_region_the_burning_monolith'},
    187: {'name': 'wh3_main_combi_region_soteks_trail'},
    188: {'name': 'wh3_main_combi_region_temple_of_elemental_winds'},
    189: {'name': 'wh3_main_combi_region_kraka_drak'},
    190: {'name': 'wh3_main_combi_region_tor_elasor'},
    191: {'name': 'wh3_main_combi_region_tor_elyr'},
    192: {'name': 'wh3_main_combi_region_karak_vlag'},
    193: {'name': 'wh3_main_combi_region_karak_vrag'},
    194: {'name': 'wh3_main_combi_region_the_cursed_jungle'},
    195: {'name': 'wh3_main_combi_region_karag_dromar'},
    196: {'name': 'wh3_main_combi_region_erengrad'},
    197: {'name': 'wh3_main_combi_region_frozen_landing'},
    198: {'name': 'wh3_main_combi_region_fort_straghov'},
    199: {'name': 'wh3_main_combi_region_monolith_of_festerlung'},
    200: {'name': 'wh3_main_combi_region_clar_karond'},
    201: {'name': 'wh3_main_combi_region_agrul_migdhal'},
    202: {'name': 'wh3_main_combi_region_the_falls_of_doom'},
    203: {'name': 'wh3_main_combi_region_castle_artois'},
    204: {'name': 'wh3_main_combi_region_tower_of_the_stars'},
    205: {'name': 'wh3_main_combi_region_chupayotl'},
    206: {'name': 'wh3_main_combi_region_karak_azul'},
    207: {'name': 'wh3_main_combi_region_brionne'},
    208: {'name': 'wh3_main_combi_region_wizard_caliphs_palace'},
    209: {'name': 'wh3_main_combi_region_the_frozen_city'},
    210: {'name': 'wh3_main_combi_region_ruins_end'},
    211: {'name': 'wh3_main_combi_region_the_high_sentinel'},
    212: {'name': 'wh3_main_combi_region_black_creek_spire'},
    213: {'name': 'wh3_main_combi_region_shattered_stone_isle'},
    214: {'name': 'wh3_main_combi_region_khemri'},
    215: {'name': 'wh3_main_combi_region_karak_zorn'},
    216: {'name': 'wh3_main_combi_region_the_black_pit'},
    217: {'name': 'wh3_main_combi_region_the_pillars_of_grungni'},
    218: {'name': 'wh3_main_combi_region_temple_of_addaioth'},
    219: {'name': 'wh3_main_combi_region_shrine_of_kurnous'},
    220: {'name': 'wh3_main_combi_region_deaths_head_monoliths'},
    221: {'name': 'wh3_main_combi_region_kauark'},
    222: {'name': 'wh3_main_combi_region_howling_rock'},
    223: {'name': 'wh3_main_combi_region_darkhold'},
    224: {'name': 'wh3_main_combi_region_tlax'},
    225: {'name': 'wh3_main_combi_region_zhanshi'},
    226: {'name': 'wh3_main_combi_region_temple_of_khaine'},
    227: {'name': 'wh3_main_combi_region_the_star_tower'},
    228: {'name': 'wh3_main_combi_region_hualotal'},
    229: {'name': 'wh3_main_combi_region_karak_norn'},
    230: {'name': 'wh3_main_combi_region_the_lost_palace'},
    231: {'name': 'wh3_main_combi_region_whitefire_tor'},
    232: {'name': 'wh3_main_combi_region_gristle_valley'},
    233: {'name': 'wh3_main_combi_region_riffraffa'},
    234: {'name': 'wh3_main_combi_region_shrine_of_the_alchemist'},
    235: {'name': 'wh3_dlc20_combi_region_glacier_encampment'},
    236: {'name': 'wh3_main_combi_region_crucible_of_delights'},
    237: {'name': 'wh3_main_combi_region_phoenix_gate'},
    238: {'name': 'wh3_main_combi_region_vale_of_titans'},
    239: {'name': 'wh3_main_combi_region_igerov'},
    240: {'name': 'wh3_main_combi_region_blood_mountain'},
    241: {'name': 'wh3_main_combi_region_the_blood_hall'},
    242: {'name': 'wh3_main_combi_region_volcanos_heart'},
    243: {'name': 'wh3_main_combi_region_altar_of_the_crimson_harvest'},
    244: {'name': 'wh3_main_combi_region_salzenmund'},
    245: {'name': 'wh3_main_combi_region_sjoktraken'},
    246: {'name': 'wh3_main_combi_region_dringorackaz'},
    247: {'name': 'wh3_main_combi_region_granite_massif'},
    248: {'name': 'wh3_main_combi_region_chimai'},
    249: {'name': 'wh3_main_combi_region_okkams_forever_maze'},
    250: {'name': 'wh3_main_combi_region_sorcerers_islands'},
    251: {'name': 'wh3_main_combi_region_the_southern_sentinels'},
    252: {'name': 'wh3_main_combi_region_chamber_of_visions'},
    253: {'name': 'wh3_main_combi_region_the_oak_of_ages'},
    254: {'name': 'wh3_main_combi_region_grey_rock_point'},
    255: {'name': 'wh3_main_combi_region_vauls_anvil_naggaroth'},
    256: {'name': 'wh3_main_combi_region_the_never_ending_chasm'},
    257: {'name': 'wh3_main_combi_region_waterfall_palace'},
    258: {'name': 'wh3_main_combi_region_fort_bergbres'},
    259: {'name': 'wh3_dlc20_combi_region_glacial_gardens'},
    260: {'name': 'wh3_main_combi_region_serpent_jetty'},
    261: {'name': 'wh3_main_combi_region_chill_road'},
    262: {'name': 'wh3_dlc20_combi_region_dragons_death'},
    263: {'name': 'wh3_main_combi_region_graeling_moot'},
    264: {'name': 'wh3_main_combi_region_li_zhu'},
    265: {'name': 'wh3_main_combi_region_snake_gate'},
    266: {'name': 'wh3_main_combi_region_port_elistor'},
    267: {'name': 'wh3_main_combi_region_eilhart'},
    268: {'name': 'wh3_main_combi_region_black_rock'},
    269: {'name': 'wh3_main_combi_region_grom_peak'},
    270: {'name': 'wh3_main_combi_region_valley_of_horns'},
    271: {'name': 'wh3_main_combi_region_celestial_monastery'},
    272: {'name': 'wh3_main_combi_region_zvorak'},
    273: {'name': 'wh3_main_combi_region_dragon_gate'},
    274: {'name': 'wh3_main_combi_region_xlanhuapec'},
    275: {'name': 'wh3_main_combi_region_slavers_point'},
    276: {'name': 'wh3_main_combi_region_kislev'},
    277: {'name': 'wh3_main_combi_region_flensburg'},
    278: {'name': 'wh3_main_combi_region_dragonhorn_mines'},
    279: {'name': 'wh3_main_combi_region_vauls_anvil_loren'},
    280: {'name': 'wh3_main_combi_region_varenka_hills'},
    281: {'name': 'wh3_main_combi_region_jade_wind_mountain'},
    282: {'name': 'wh3_main_combi_region_karak_kadrin'},
    283: {'name': 'wh3_main_combi_region_granite_spikes'},
    284: {'name': 'wh3_main_combi_region_xlanzec'},
    285: {'name': 'wh3_main_combi_region_bloodwind_keep'},
    286: {'name': 'wh3_main_combi_region_dotternbach'},
    287: {'name': 'wh3_main_combi_region_dietershafen'},
    288: {'name': 'wh3_main_combi_region_nuln'},
    289: {'name': 'wh3_main_combi_region_karak_krakaten'},
    290: {'name': 'wh3_main_combi_region_mountain_pass'},
    291: {'name': 'wh3_main_combi_region_citadel_of_lead'},
    292: {'name': 'wh3_main_combi_region_gnobbly_gorge'},
    293: {'name': 'wh3_main_combi_region_bitterstone_mine'},
    294: {'name': 'wh3_main_combi_region_quetza'},
    295: {'name': 'wh3_main_combi_region_haichai'},
    296: {'name': 'wh3_main_combi_region_oyxl'},
    297: {'name': 'wh3_main_combi_region_avethir'},
    298: {'name': 'wh3_main_combi_region_akendorf'},
    299: {'name': 'wh3_main_combi_region_khymerica_spire'},
    300: {'name': 'wh3_dlc23_combi_region_gash_kadrak'},
    301: {'name': 'wh3_main_combi_region_castle_alexandronov'},
    302: {'name': 'wh3_main_combi_region_eagle_gate'},
    303: {'name': 'wh3_main_combi_region_spite_reach'},
    304: {'name': 'wh3_main_combi_region_zharr_naggrund'},
    305: {'name': 'wh3_main_combi_region_eschen'},
    306: {'name': 'wh3_main_combi_region_montenas'},
    307: {'name': 'wh3_main_combi_region_al_haikk'},
    308: {'name': 'wh3_main_combi_region_drackla_spire'},
    309: {'name': 'wh3_main_combi_region_turtle_gate'},
    310: {'name': 'wh3_dlc20_combi_region_krudenwald'},
    311: {'name': 'wh3_main_combi_region_tor_achare'},
    312: {'name': 'wh3_main_combi_region_quittax'},
    313: {'name': 'wh3_dlc23_combi_region_uzkulak_port'},
    314: {'name': 'wh3_main_combi_region_karak_ungor'},
    315: {'name': 'wh3_main_combi_region_bitter_bay'},
    316: {'name': 'wh3_main_combi_region_altdorf'},
    317: {'name': 'wh3_main_combi_region_altar_of_facades'},
    318: {'name': 'wh3_main_combi_region_the_sacred_pools'},
    319: {'name': 'wh3_main_combi_region_the_skull_carvers_abode'},
    320: {'name': 'wh3_main_combi_region_the_haunted_forest'},
    321: {'name': 'wh3_main_combi_region_temple_of_skulls'},
    322: {'name': 'wh3_main_combi_region_dusk_peaks'},
    323: {'name': 'wh3_main_combi_region_yetchitch'},
    324: {'name': 'wh3_main_combi_region_itza'},
    325: {'name': 'wh3_main_combi_region_grung_zint'},
    326: {'name': 'wh3_main_combi_region_bhagar'},
    327: {'name': 'wh3_main_combi_region_crag_halls_of_findol'},
    328: {'name': 'wh3_main_combi_region_el_kalabad'},
    329: {'name': 'wh3_main_combi_region_thrice_cursed_peak'},
    330: {'name': 'wh3_main_combi_region_cragroth_deep'},
    331: {'name': 'wh3_main_combi_region_citadel_of_dusk'},
    332: {'name': 'wh3_main_combi_region_crookback_mountain'},
    333: {'name': 'wh3_main_combi_region_volksgrad'},
    334: {'name': 'wh3_main_combi_region_hoteks_column'},
    335: {'name': 'wh3_main_combi_region_the_crystal_spires'},
    336: {'name': 'wh3_main_combi_region_ming_zhu'},
    337: {'name': 'wh3_main_combi_region_parravon'},
    338: {'name': 'wh3_main_combi_region_barak_varr'},
    339: {'name': 'wh3_main_combi_region_gaean_vale'},
    340: {'name': 'wh3_main_combi_region_fuming_serpent'},
    341: {'name': 'wh3_main_combi_region_village_of_the_tigermen'},
    342: {'name': 'wh3_main_combi_region_castle_bastonne'},
    343: {'name': 'wh3_main_combi_region_amblepeak'},
    344: {'name': 'wh3_main_combi_region_har_kaldra'},
    345: {'name': 'wh3_main_combi_region_gisoreux'},
    346: {'name': 'wh3_main_combi_region_li_temple'},
    347: {'name': 'wh3_main_combi_region_foundry_of_bones'},
    348: {'name': 'wh3_main_combi_region_black_fang'},
    349: {'name': 'wh3_main_combi_region_aarnau'},
    350: {'name': 'wh3_main_combi_region_eagle_eyries'},
    351: {'name': 'wh3_main_combi_region_gryphon_wood'},
    352: {'name': 'wh3_main_combi_region_carroburg'},
    353: {'name': 'wh3_main_combi_region_xing_po'},
    354: {'name': 'wh3_main_combi_region_praag'},
    355: {'name': 'wh3_main_combi_region_tower_of_lysean'},
    356: {'name': 'wh3_main_combi_region_naggarond'},
    357: {'name': 'wh3_main_combi_region_great_hall_of_greasus'},
    358: {'name': 'wh3_main_combi_region_the_blighted_grove'},
    359: {'name': 'wh3_main_combi_region_talabheim'},
    360: {'name': 'wh3_main_combi_region_rasetra'},
    361: {'name': 'wh3_main_combi_region_the_twisted_towers'},
    362: {'name': 'wh3_main_combi_region_the_bone_gulch'},
    363: {'name': 'wh3_main_combi_region_tlaxtlan'},
    364: {'name': 'wh3_main_combi_region_the_sentinel_of_time'},
    365: {'name': 'wh3_main_combi_region_ubersreik'},
    366: {'name': 'wh3_main_combi_region_fort_ostrosk'},
    367: {'name': 'wh3_main_combi_region_plain_of_tuskers'},
    368: {'name': 'wh3_main_combi_region_volulltrax'},
    369: {'name': 'wh3_main_combi_region_gronti_mingol'},
    370: {'name': 'wh3_main_combi_region_yhetee_peak'},
    371: {'name': 'wh3_main_combi_region_bay_of_blades'},
    372: {'name': 'wh3_main_combi_region_unicorn_gate'},
    373: {'name': 'wh3_main_combi_region_ironspike'},
    374: {'name': 'wh3_main_combi_region_teotiqua'},
    375: {'name': 'wh3_main_combi_region_shang_wu'},
    376: {'name': 'wh3_main_combi_region_plain_of_spiders'},
    377: {'name': 'wh3_main_combi_region_bloodpeak'},
    378: {'name': 'wh3_main_combi_region_weismund'},
    379: {'name': 'wh3_main_combi_region_gnashraks_lair'},
    380: {'name': 'wh3_main_combi_region_evershale'},
    381: {'name': 'wh3_main_combi_region_scarpels_lair'},
    382: {'name': 'wh3_main_combi_region_shroktak_mount'},
    383: {'name': 'wh3_main_combi_region_ssildra_tor'},
    384: {'name': 'wh3_main_combi_region_naglfari_plain'},
    385: {'name': 'wh3_main_combi_region_tor_saroir'},
    386: {'name': 'wh3_main_combi_region_dai_cheng'},
    387: {'name': 'wh3_main_combi_region_ice_rock_gorge'},
    388: {'name': 'wh3_main_combi_region_bridge_of_heaven'},
    389: {'name': 'wh3_main_combi_region_marienburg'},
    390: {'name': 'wh3_main_combi_region_ash_ridge_mountains'},
    391: {'name': 'wh3_main_combi_region_quenelles'},
    392: {'name': 'wh3_main_combi_region_axlotl'},
    393: {'name': 'wh3_main_combi_region_plesk'},
    394: {'name': 'wh3_main_combi_region_the_witchwood'},
    395: {'name': 'wh3_main_combi_region_jungles_of_chian'},
    396: {'name': 'wh3_main_combi_region_golden_ziggurat'},
    397: {'name': 'wh3_main_combi_region_skeggi'},
    398: {'name': 'wh3_main_combi_region_the_moot'},
    399: {'name': 'wh3_main_combi_region_har_ganeth'},
    400: {'name': 'wh3_main_combi_region_karag_orrud'},
    401: {'name': 'wh3_main_combi_region_mount_athull'},
    402: {'name': 'wh3_main_combi_region_worlds_edge_archway'},
    403: {'name': 'wh3_main_combi_region_black_fortress'},
    404: {'name': 'wh3_main_combi_region_port_reaver'},
    405: {'name': 'wh3_main_combi_region_chaqua'},
    406: {'name': 'wh3_main_combi_region_vitevo'},
    407: {'name': 'wh3_main_combi_region_morgheim'},
    408: {'name': 'wh3_main_combi_region_kradtommen'},
    409: {'name': 'wh3_main_combi_region_ekrund'},
    410: {'name': 'wh3_main_combi_region_khazid_bordkarag'},
    411: {'name': 'wh3_main_combi_region_shang_yang'},
    412: {'name': 'wh3_main_combi_region_blacklight_tower'},
    413: {'name': 'wh3_main_combi_region_the_howling_citadel'},
    414: {'name': 'wh3_main_combi_region_monolith_of_bubonicus'},
    415: {'name': 'wh3_main_combi_region_statues_of_the_gods'},
    416: {'name': 'wh3_main_combi_region_infernius'},
    417: {'name': 'wh3_main_combi_region_subatuun'},
    418: {'name': 'wh3_main_combi_region_novchozy'},
    419: {'name': 'wh3_main_combi_region_gorssel'},
    420: {'name': 'wh3_main_combi_region_po_mei'},
    421: {'name': 'wh3_main_combi_region_pahuax'},
    422: {'name': 'wh3_main_combi_region_karak_azgaraz'},
    423: {'name': 'wh3_main_combi_region_vauls_anvil_ulthuan'},
    424: {'name': 'wh3_main_combi_region_the_gates_of_zharr'},
    425: {'name': 'wh3_main_combi_region_ziggurat_of_dawn'},
    426: {'name': 'wh3_main_combi_region_karak_bhufdar'},
    427: {'name': 'wh3_main_combi_region_nonchang'},
    428: {'name': 'wh3_main_combi_region_wissenburg'},
    429: {'name': 'wh3_main_combi_region_fortress_of_dawn'},
    430: {'name': 'wh3_main_combi_region_fyrus'},
    431: {'name': 'wh3_main_combi_region_the_volary'},
    432: {'name': 'wh3_main_combi_region_altar_of_the_horned_rat'},
    433: {'name': 'wh3_main_combi_region_cliff_of_beasts'},
    434: {'name': 'wh3_main_combi_region_fallen_king_mountain'},
    435: {'name': 'wh3_main_combi_region_forest_of_gloom'},
    436: {'name': 'wh3_main_combi_region_bilious_cliffs'},
    437: {'name': 'wh3_main_combi_region_baleful_hills'},
    438: {'name': 'wh3_main_combi_region_the_silvered_tower_of_sorcerers'},
    439: {'name': 'wh3_main_combi_region_silver_pinnacle'},
    440: {'name': 'wh3_main_combi_region_konquata'},
    441: {'name': 'wh3_main_combi_region_castle_drakenhof'},
    442: {'name': 'wh3_main_combi_region_hidden_landing'},
    443: {'name': 'wh3_main_combi_region_sabre_mountain'},
    444: {'name': 'wh3_main_combi_region_bamboo_crossing'},
    445: {'name': 'wh3_main_combi_region_bilbali'},
    446: {'name': 'wh3_main_combi_region_pox_marsh'},
    447: {'name': 'wh3_main_combi_region_floating_pyramid'},
    448: {'name': 'wh3_main_combi_region_forest_of_arnheim'},
    449: {'name': 'wh3_main_combi_region_kings_glade'},
    450: {'name': 'wh3_main_combi_region_waili_village'},
    451: {'name': 'wh3_main_combi_region_antoch'},
    452: {'name': 'wh3_main_combi_region_doom_glade'},
    453: {'name': 'wh3_main_combi_region_valayas_sorrow'},
    454: {'name': 'wh3_main_combi_region_the_forbidden_citadel'},
    455: {'name': 'wh3_main_combi_region_shi_wu'},
    456: {'name': 'wh3_main_combi_region_karak_dum'},
    457: {'name': 'wh3_main_combi_region_springs_of_eternal_life'},
    458: {'name': 'wh3_main_combi_region_spektazuma'},
    459: {'name': 'wh3_main_combi_region_plain_of_dogs'},
    460: {'name': 'wh3_main_combi_region_bordeleaux'},
    461: {'name': 'wh3_main_combi_region_lothern'},
    462: {'name': 'wh3_main_combi_region_tower_of_ashung'},
    463: {'name': 'wh3_main_combi_region_titans_notch'},
    464: {'name': 'wh3_main_combi_region_averheim'},
    465: {'name': 'wh3_main_combi_region_temple_of_tlencan'},
    466: {'name': 'wh3_main_combi_region_dragon_fang_mount'},
    467: {'name': 'wh3_main_combi_region_karak_azgal'},
    468: {'name': 'wh3_main_combi_region_tlanxla'},
    469: {'name': 'wh3_main_combi_region_lahmia'},
    470: {'name': 'wh3_main_combi_region_misty_mountain'},
    471: {'name': 'wh3_main_combi_region_tralinia'},
    472: {'name': 'wh3_main_combi_region_khazid_irkulaz'},
    473: {'name': 'wh3_main_combi_region_sun_tree_glades'},
    474: {'name': 'wh3_main_combi_region_hag_graef'},
    475: {'name': 'wh3_main_combi_region_arnheim'},
    476: {'name': 'wh3_main_combi_region_the_tower_of_khrakk'},
    477: {'name': 'wh3_main_combi_region_mount_arachnos'},
    478: {'name': 'wh3_main_combi_region_the_sentinels'},
    479: {'name': 'wh3_main_combi_region_oreons_camp'},
    480: {'name': 'wh3_main_combi_region_tor_anroc'},
    481: {'name': 'wh3_main_combi_region_nan_li'},
    482: {'name': 'wh3_main_combi_region_whitepeak'},
    483: {'name': 'wh3_main_combi_region_couronne'},
    484: {'name': 'wh3_main_combi_region_mount_thug'},
    485: {'name': 'wh3_main_combi_region_the_challenge_stone'},
    486: {'name': 'wh3_main_combi_region_petrified_forest'},
    487: {'name': 'wh3_main_combi_region_ashrak'},
    488: {'name': 'wh3_main_combi_region_mount_squighorn'},
    489: {'name': 'wh3_main_combi_region_monolith_of_flesh'},
    490: {'name': 'wh3_main_combi_region_karak_ziflin'},
    491: {'name': 'wh3_main_combi_region_dawns_light'},
    492: {'name': 'wh3_main_combi_region_myrmidens'},
    493: {'name': 'wh3_main_combi_region_kaiax'},
    494: {'name': 'wh3_main_combi_region_mount_gunbad'},
    495: {'name': 'wh3_main_combi_region_castle_von_rauken'},
    496: {'name': 'wh3_main_combi_region_temple_of_heimkel'},
    497: {'name': 'wh3_main_combi_region_isle_of_the_crimson_skull'},
    498: {'name': 'wh3_main_combi_region_port_of_secrets'},
    499: {'name': 'wh3_main_combi_region_galbaraz'},
    500: {'name': 'wh3_main_combi_region_the_tower_of_flies'},
    501: {'name': 'wh3_main_combi_region_the_forest_of_decay'},
    502: {'name': 'wh3_main_combi_region_monument_of_the_moon'},
    503: {'name': 'wh3_main_combi_region_magritta'},
    504: {'name': 'wh3_main_combi_region_zarakzil'},
    505: {'name': 'wh3_main_combi_region_serpent_coast'},
    506: {'name': 'wh3_main_combi_region_the_golden_colossus'},
    507: {'name': 'wh3_main_combi_region_icespewer'},
    508: {'name': 'wh3_main_combi_region_waldenhof'},
    509: {'name': 'wh3_main_combi_region_altar_of_ultimate_darkness'},
    510: {'name': 'wh3_main_combi_region_stormhenge'},
    511: {'name': 'wh3_main_combi_region_tor_anlec'},
    512: {'name': 'wh3_main_combi_region_fire_mouth'},
    513: {'name': 'wh3_main_combi_region_blizzardpeak'},
    514: {'name': 'wh3_main_combi_region_iron_rock'},
    515: {'name': 'wh3_main_combi_region_pigbarter'},
    516: {'name': 'wh3_main_combi_region_the_maw_gate'},
    517: {'name': 'wh3_main_combi_region_temple_of_kara'},
    518: {'name': 'wh3_dlc23_combi_region_fort_dorznye_vort'},
    519: {'name': 'wh3_main_combi_region_sentinels_of_xeti'},
    520: {'name': 'wh3_main_combi_region_verdanos'},
    521: {'name': 'wh3_main_combi_region_pfeildorf'},
    522: {'name': 'wh3_main_combi_region_matorca'},
    523: {'name': 'wh3_main_combi_region_shrine_of_asuryan'},
    524: {'name': 'wh3_main_combi_region_iron_storm'},
    525: {'name': 'wh3_main_combi_region_nagrar'},
    526: {'name': 'wh3_main_combi_region_hexoatl'},
    527: {'name': 'wh3_main_combi_region_the_great_arena'},
    528: {'name': 'wh3_main_combi_region_castle_of_splendour'},
    529: {'name': 'wh3_main_combi_region_shiyamas_rest'},
    530: {'name': 'wh3_main_combi_region_tor_sethai'},
    531: {'name': 'wh3_main_combi_region_grotrilexs_glare_lighthouse'},
    532: {'name': 'wh3_main_combi_region_castle_templehof'},
    533: {'name': 'wh3_main_combi_region_luccini'},
    534: {'name': 'wh3_main_combi_region_grunburg'},
    535: {'name': 'wh3_main_combi_region_brass_keep'},
    536: {'name': 'wh3_main_combi_region_tyrant_peak'},
    537: {'name': 'wh3_main_combi_region_pack_ice_bay'},
    538: {'name': 'wh3_main_combi_region_sulpharets'},
    539: {'name': 'wh3_dlc23_combi_region_blasted_expanse'},
    540: {'name': 'wh3_main_combi_region_angerrial'},
    541: {'name': 'wh3_main_combi_region_dagraks_end'},
    542: {'name': 'wh3_main_combi_region_mount_grey_hag'},
    543: {'name': 'wh3_main_combi_region_wreckers_point'},
    544: {'name': 'wh3_main_combi_region_sudenburg'},
    545: {'name': 'wh3_main_combi_region_middenstag'},
    546: {'name': 'wh3_main_combi_region_crooked_fang_fort'},
    547: {'name': 'wh3_main_combi_region_zhizhu'},
    548: {'name': 'wh3_main_combi_region_the_sinhall_monolith'},
    549: {'name': 'wh3_main_combi_region_uzkulak'},
    550: {'name': 'wh3_main_combi_region_gorger_rock'},
    551: {'name': 'wh3_main_combi_region_fu_chow'},
    552: {'name': 'wh3_main_combi_region_the_golden_tower'},
    553: {'name': 'wh3_main_combi_region_shi_long'},
    554: {'name': 'wh3_main_combi_region_the_high_place'},
    555: {'name': 'wh3_main_combi_region_doomkeep'},
    556: {'name': 'wh3_main_combi_region_the_fetid_catacombs'},
    557: {'name': 'wh3_main_combi_region_varg_camp'},
    558: {'name': 'wh3_main_combi_region_circle_of_destruction'},
    559: {'name': 'wh3_main_combi_region_the_twisted_glade'},
    560: {'name': 'wh3_main_combi_region_ironfrost'},
    561: {'name': 'wh3_main_combi_region_the_tower_of_torment'},
    562: {'name': 'wh3_main_combi_region_black_crag'},
    563: {'name': 'wh3_main_combi_region_karag_dron'},
    564: {'name': 'wh3_main_combi_region_great_turtle_isle'},
    565: {'name': 'wh3_main_combi_region_the_monoliths'}
}