from combat.Move import Move, MoveCategory, PokemonType
from combat.constants.move_effects import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Pokemon import Pokemon

Sing = Move("Sing", 0, 55, [PokemonType.NORMAL], MoveCategory.STATUS, False, [MoveInflictSleep()])
Tackle = Move("Tackle", 40, 95, [PokemonType.NORMAL], MoveCategory.PHYSICAL, True)
Thunderbolt = Move("Thunderbolt", 90, 100, [PokemonType.ELECTRIC], MoveCategory.SPECIAL, False, [MoveInflictParalyzeChance(30)])
Takedown = Move("Takedown", 90, 85, [PokemonType.NORMAL], MoveCategory.PHYSICAL, True, recoil_percent=25)


def imagine_effect(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
    if attacker.get_hp() == attacker.get_max_hp():
        return self.normal_use(self, attacker, defender)
    else:
        import random
        if random.randint(0, 100) > 50:
            es = [
                MoveInflictParalyzeChance(100).affect(attacker, attacker, None),
                MoveInflictExactDamage(30).affect(attacker, attacker, None)
            ]
            return es
        else:
            return Event(EventType.ATTACK_FAILED, EventData(attacker=attacker, defender=defender))


# A move which has 50% accuracy, and if hits, does both recoil damage and heals the attacker, it also has 50% chance of
# putting the defender into paralysis. The move also only works if the user is at full hp. Otherwise it has 50% chance to
# paralyse and do 30 damage to the user
Imagine = Move("Img", 50, 50, [PokemonType.GRASS], MoveCategory.SPECIAL, True, recoil_percent=50, absorb_percent=25, effects=[MoveInflictParalyzeChance(50)], use_function=imagine_effect)