from combat.Move import Move, MoveCategory, PokemonType, MultiHit
from combat.constants.move_effects import *
from typing import TYPE_CHECKING
from random import randint
from combat.constants.pokemon_types import type_multiplier

if TYPE_CHECKING:
    from Pokemon import Pokemon


Sing = Move("Sing", 0, 55, PokemonType.NORMAL, MoveCategory.STATUS, effects=[MoveInflictSleep()])
Tackle = Move("Tackle", 40, 95, PokemonType.NORMAL, MoveCategory.PHYSICAL)
KarateChop = Move("Karate Chop", 50, 100, PokemonType.FIGHTING, MoveCategory.PHYSICAL, crit_chance=30)
DoubleSlap = Move("Double Slap", 15, 85, PokemonType.NORMAL, MoveCategory.PHYSICAL, use_function=MultiHit.multi_hit)
CometPunch = Move("Comet Punch", 18, 85, PokemonType.NORMAL, MoveCategory.PHYSICAL, use_function=MultiHit.multi_hit)
MegaPunch = Move("MegaPunch", 80, 85, PokemonType.NORMAL, MoveCategory.PHYSICAL)
PayDay = Move("PayDay", 40, 100, PokemonType.NORMAL, MoveCategory.PHYSICAL, False)  # TODO: Payday effect
FirePunch = Move("Fire Punch", 75, 100, PokemonType.FIRE, MoveCategory.PHYSICAL, effects=[MoveInflictBurnChance(10)])
Thunderbolt = Move("Thunderbolt", 90, 100, PokemonType.ELECTRIC, MoveCategory.SPECIAL, effects=[MoveInflictParalyzeChance(30)])
Takedown = Move("Takedown", 90, 85, PokemonType.NORMAL, MoveCategory.PHYSICAL, recoil_percent=25)
