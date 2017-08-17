from combat.Move import Move, MoveCategory, PokemonType
from combat.constants.move_effects import *

Sing = Move("Sing", 0, 55, [PokemonType.NORMAL], MoveCategory.STATUS, False, [MoveInflictSleep()])
Tackle = Move("Tackle", 40, 95, [PokemonType.NORMAL], MoveCategory.PHYSICAL, True, [])
Thunderbolt = Move("Thunderbolt", 90, 100, [PokemonType.ELECTRIC], MoveCategory.SPECIAL, False, [MoveInflictParalyzeChance(30)])