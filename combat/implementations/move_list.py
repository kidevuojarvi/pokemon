from combat.Move import Move, MoveCategory, PokemonType
from combat.constants.move_effects import *

Sing = Move("Sing", 0, 60, [PokemonType.NORMAL], MoveCategory.STATUS, False, [MoveEffect(MoveInflictSleep)])
