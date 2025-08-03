# Total War: Warhammer 3 Archipelago
## What does randomization do to this game?
Archipelago for Total War: Warhammer randomizes the start position and AI Personalities of all factions present on the map at game start. Every Settlement is considered a check which gets send out when choosing a post-battle option or owning the settlements via other means, including vassals and alliances.

Logic gates are included by Diplomatic Sphere items. The range in which diplomacy, including war declaration, is restricted and gets extended by finding Sphere items, making sure you dont have to do a world conquest at game start.

Furthermore units, buildings, technologies and some faction mechanics can be shuffled into the item pool which causes them to be locked until the corresponding archipelago item is received.

There are a few changes that the Archipelago mod introduces in order to make this playable/fun aswell as some recommended submods. These are detailed in the FAQ section below.

## What is the goal of Total War: Warhammer 3 when randomized?
The goal of randomized Total War: Warhammer 3 is to find all Orbs of Domination in the Multiworld. The number of Orbs can be changed in the yaml settings.

## Which items can be in another player's world?
All units, buildings, technologies and faction mechanics can be found in another player's world, if shuffle for those is enabled. Also more diplomacy range and Orbs of Domination are hidden throughout the multiworld as well as lots of creative filler and traps items that can severly change the way your run plays out if enabled.

## What does another world's item look like in Civilization VI?
Each item from another world is represented as a settlement to conquer.

## When the player receives an item, what happens?
The received items are shown in the archipelago client and take effect immediately if in-game or after loading a save file or starting a new campaign. On new campaign all received items activate right away but traps are disabled. You will also get the regular popup in case you were sent equipment or similar things which cause a popup in vanilla.

## FAQs

## I used the default yaml and my stuff was not shuffled? 

Sadly Dev is a weirdo and picked shuffle false, progressive on as default setting while progressive requires shuffle to be on. Make sure to activate the shuffles you want, else stuff wont be locked.

## Do I need the DLCs to play this?

You only need the corresponding DLC with you want to play a DLC Faction, as in vanilla

## I am High Elves and spawned in the Chaos Wastelands. I cant make money, recruitment takes ages and my order is non-existent. This sucks. 

Consider using the no climate penalties mod (or any similar mod you like). We do recommend using some climate mod with this to prevent these kinds of situations.

## I am Karl Franz, the whole Empire belongs to Lizards and Chaos Dwarfs and I am stuck in Lustria. This sucks. 

Consider using the Archipelago Remove Faction Mechanic Debuffs Mods. This mod for archipelago disables Debuffs related to not being at the right position on the map like Imperial Mandate for Empire or the doughnut mechanic for Avelorn. While these are fun mechanics they obviously dont work in context of random spawn points.

## Can I play Woodelves?

Woodelves are guaranteed to start at a random tree. You are fine.

## Can I play Warriors of Chaos?

While Warriors of Chaos are not guaranteed to own a Dark Fortress, the warband mechanic allows for early game recruitment, enabling you to hopefully conquer a Dark Fortress in your vicinity. There are maps with all Dark Fortresses marked on them online. If you happen to spawn in Lustria or Araby consider rerolling or using a mod that creates Dark Fortresses in your area. A submod might solve this eventually.

## Does this work with Multiplayer?

Multiplayer Campaign is a planned feature down the road. You can play a coop campaign with randomized start positions and one player playing the archipelago slot and the other(s) playing normally, I believe. If you test coop please tell us how it went.

## I got Skarbrand's unique weapon. I obviously cant equip it.

Use the No Requirement Sub Mod [link]. Note: This messes up the tool tip. If you cant see what the item does you can see its effects once you equip it.

## Does this work with other mods?

A lot of mods seem to work without issues combined with the main mod, but mods that add units, buildings or techs or are major overhauls dont get their content shuffled and might break things. Some of the optional submods do interfere with the tables quite a lot and are therefor probably not compatible with other mods touching the same content.

## "How does DeathLink work? Am I going to have to start a new game every time one of my friends dies?"

Not yet as we havent fully figure out on how it should work yet. Stay tuned.

## "I enabled a shuffle option but have no idea what the item I got unlocks for me!"

Sadly translating every single key of every single faction is a lot of work, but we are working on human readability. You are always welcome to ask for something in our discord thread [link].

## So... what options and submods should I even play with?

Glad you asked! Have a quick guide on what stuff does! 

**starting_faction**: Pick who you wanna play!

**faction_shuffle**: randomize starting positions. This is kinda the main feature so we recommend turning it on.

**max_settlement_distance**: Tells the start randomizer how far apart settlements of the same faction are allowed to be. 50 is next to each other, 1500 is somewhere on the same planet.

**tech_shuffle**: Should your tech tree be unlocked by archipelago items? Increases difficulty by restricting your research.
**progressive_technologies**: Requires tech_shuffle to be on! Every step further into your tech tree is a progressive item. Else every single tech is a separate item. 

If you play with progressive tech off you can use the Archipelago_Remove_Tech_Requirements Mod [Link] which lets you research techs out of order so you dont have to wait for the whole chain to be found before researching a late game tech you found.

**building_shuffle**: Should your buildings be unlocked by archipelago items?
**progressive_buildings**: Requires building_shuffle to be on! Instead of finding every single building seperately find progressive items unlocking the next building for each specific building chain. Setting this to progressive is recommended.

**unit_shuffle**: Should your units be unlocked by archipelago items?
**progressive_units**: Requires unit_shuffle to be on! Instead of unlocking every unit separately unlock tier 1-5 by progressive items for each unit type (progressive infantry, progressive cavalry, progressive monsters etc.). Both options are good to play. I would personally suggest to not set buildings and units to both progressive off as this leads to a lot of prerequisites for building units.

**starting_tier**: Starts you out with buildings and units of this tier already unlocked. (this will be separated in a later release)

**spheres_option**: How many Spheres of Influence your map is divided into and need to be found.
**spheres_distance**: The distance - measured from your first settlement - each Sphere of Influence unlocks.
**sphere_world**: If the last sphere always results in world conquest

Spheres do limit your diplomance and therefor which settlements you are able to take. Small Spheres allow you to bk. If sphere_world is set to off the number of spheres times the distance determines the amount of checks. As the start position is (probably) randomized and might be a corner of the map the amount of checks is sadly not determinable pre-gen. 

Rule of thumb: if spheres * distance ~1300 you are guaranteed to have every settlement included in your game, regardless of spawn position. This means ~700 and a spawn in the middle of the map also includes every settlement (as the distance extends in all directions, so the diameter is >1300 again. Just try to imagine a circle on the world map)

**balance_spheres**: Ensures every sphere does include a minimum amount of unlocks. As spheres get progressively bigger this mostly ensures early game unlocks in a solo game. Note this is implemented via archipelago logic so it forces some of your unlocks to be early somewhere in the multiworld. It does not force them to be local i.e. literally inside your sphere. Turning this on is heavily recommended.

**balance_spheres_percentage**: Takes the total amount of checks per sphere and sets the stated % of items to be unlock items. Again - this does only effect the archipelago logic. Higher percentage results in more early game unlocks.

**balance_spheres_max_unlocks**: Max unlocks per sphere. Just ignore.

**goal**: Your goal condition. Currently only collecting the Orbs of Domination is supported.
domination_option: How many Orbs of Domination need to be found

**filler and traps**: Set to your own liking. Note that "strong" can be gamechangingly strong or even kill your run (you can reload a previous save, traps wont trigger twice). Filler items include all equipment items. We recommend the No Requirement Archipelago Sub Mod [Link] to make sure you can equip every item you get.

**RandomizePersonalities**: Give AI faction random personalities. Makes the game less predictable and can lead to interesting situations.

**ritual_shuffle**: If you want to unlock certain faction mechanics via archipelago items. Highly experimental and because of the vast amount of different faction mechanics the faction you decided to play probably wasnt tested yet. Please report in our discord thread if it works or if you encountered any problems.


## Recommended Submods: 

Archipelago_Remove_Tech_Requirements: Lets you research all tech in any order. This is specifically intended to be used when using shuffled non-progressive tech so you can research every tech once it gets send to you!

Archipelago Remove Faction Mechanic Debuffs: Removes the Debuffs from Avelorn, Empire factions, Clan Angrund, Skarsnik and Oxyotl which are related to specific places on the map you probably cant reach.

No Requirement Archipelago Sub Mod: Lets you equip all items, even if they are restricted to a very different Legendary Lord normally.

No climate penalties: Removes all climate penalties so your start position is not as bad as it seems.

# [Archipelago](https://archipelago.gg) ![Discord Shield](https://discordapp.com/api/guilds/731205301247803413/widget.png?style=shield) | [Install](https://github.com/ArchipelagoMW/Archipelago/releases)

Archipelago provides a generic framework for developing multiworld capability for game randomizers. In all cases,
presently, Archipelago is also the randomizer itself.

Currently, the following games are supported:

* The Legend of Zelda: A Link to the Past
* Factorio
* Subnautica
* Risk of Rain 2
* The Legend of Zelda: Ocarina of Time
* Timespinner
* Super Metroid
* Secret of Evermore
* Final Fantasy
* Rogue Legacy
* VVVVVV
* Raft
* Super Mario 64
* Meritous
* Super Metroid/Link to the Past combo randomizer (SMZ3)
* ChecksFinder
* ArchipIDLE
* Hollow Knight
* The Witness
* Sonic Adventure 2: Battle
* Starcraft 2
* Donkey Kong Country 3
* Dark Souls 3
* Super Mario World
* Pokémon Red and Blue
* Hylics 2
* Overcooked! 2
* Zillion
* Lufia II Ancient Cave
* Blasphemous
* Wargroove
* Stardew Valley
* The Legend of Zelda
* The Messenger
* Kingdom Hearts 2
* The Legend of Zelda: Link's Awakening DX
* Clique
* Adventure
* DLC Quest
* Noita
* Undertale
* Bumper Stickers
* Mega Man Battle Network 3: Blue Version
* Muse Dash
* DOOM 1993
* Terraria
* Lingo
* Pokémon Emerald
* DOOM II
* Shivers
* Heretic
* Landstalker: The Treasures of King Nole
* Final Fantasy Mystic Quest
* TUNIC
* Kirby's Dream Land 3
* Celeste 64
* Castlevania 64
* A Short Hike
* Yoshi's Island
* Mario & Luigi: Superstar Saga
* Bomb Rush Cyberfunk
* Aquaria
* Yu-Gi-Oh! Ultimate Masters: World Championship Tournament 2006
* A Hat in Time
* Old School Runescape
* Kingdom Hearts 1
* Mega Man 2
* Yacht Dice
* Faxanadu
* Saving Princess
* Castlevania: Circle of the Moon
* Inscryption
* Civilization VI
* The Legend of Zelda: The Wind Waker
* Jak and Daxter: The Precursor Legacy
* Super Mario Land 2: 6 Golden Coins
* shapez

For setup and instructions check out our [tutorials page](https://archipelago.gg/tutorial/).
Downloads can be found at [Releases](https://github.com/ArchipelagoMW/Archipelago/releases), including compiled
windows binaries.

## History

Archipelago is built upon a strong legacy of brilliant hobbyists. We want to honor that legacy by showing it here.
The repositories which Archipelago is built upon, inspired by, or otherwise owes its gratitude to are:

* [bonta0's MultiWorld](https://github.com/Bonta0/ALttPEntranceRandomizer/tree/multiworld_31)
* [AmazingAmpharos' Entrance Randomizer](https://github.com/AmazingAmpharos/ALttPEntranceRandomizer)
* [VT Web Randomizer](https://github.com/sporchia/alttp_vt_randomizer)
* [Dessyreqt's alttprandomizer](https://github.com/Dessyreqt/alttprandomizer)
* [Zarby89's](https://github.com/Ijwu/Enemizer/commits?author=Zarby89)
  and [sosuke3's](https://github.com/Ijwu/Enemizer/commits?author=sosuke3) contributions to Enemizer, which make up the
  vast majority of Enemizer contributions.

We recognize that there is a strong community of incredibly smart people that have come before us and helped pave the
path. Just because one person's name may be in a repository title does not mean that only one person made that project
happen. We can't hope to perfectly cover every single contribution that lead up to Archipelago, but we hope to honor
them fairly.

### Path to the Archipelago

Archipelago was directly forked from bonta0's `multiworld_31` branch of ALttPEntranceRandomizer (this project has a
long legacy of its own, please check it out linked above) on January 12, 2020. The repository was then named to
_MultiWorld-Utilities_ to better encompass its intended function. As Archipelago matured, then known as
"Berserker's MultiWorld" by some, we found it necessary to transform our repository into a root level repository
(as opposed to a 'forked repo') and change the name (which came later) to better reflect our project.

## Running Archipelago

For most people, all you need to do is head over to
the [releases page](https://github.com/ArchipelagoMW/Archipelago/releases), then download and run the appropriate
installer, or AppImage for Linux-based systems.

If you are a developer or are running on a platform with no compiled releases available, please see our doc on
[running Archipelago from source](docs/running%20from%20source.md).

## Related Repositories

This project makes use of multiple other projects. We wouldn't be here without these other repositories and the
contributions of their developers, past and present.

* [z3randomizer](https://github.com/ArchipelagoMW/z3randomizer)
* [Enemizer](https://github.com/Ijwu/Enemizer)
* [Ocarina of Time Randomizer](https://github.com/TestRunnerSRL/OoT-Randomizer)

## Contributing

To contribute to Archipelago, including the WebHost, core program, or by adding a new game, see our
[Contributing guidelines](/docs/contributing.md).

## FAQ

For Frequently asked questions, please see the website's [FAQ Page](https://archipelago.gg/faq/en/).

## Code of Conduct

Please refer to our [code of conduct](/docs/code_of_conduct.md).
