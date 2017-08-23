from combat.Move import Move, MoveCategory, PokemonType
from combat.constants.move_effects import *
from typing import TYPE_CHECKING
from random import randint
from combat.constants.pokemon_types import type_multiplier

if TYPE_CHECKING:
    from Pokemon import Pokemon


# TODO: Maybe refactor multi hit entirely into move class?
def multi_hit(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
    def multi_hit_hits(ed: "EventData"):
        def multi_hit_times(ed: "EventData"):
            def multi_hit_damages(ed: "EventData"):
                return [self.attack_hits(ed) for _ in range(ed.multiplier)]
            r = randint(0, 5)
            times = [2, 2, 3, 3, 4, 5][r]
            return Event(EventType.MULTI_HIT_TIMES,
                         EventData(multiplier=times, attacker=attacker, defender=defender,
                                   function=multi_hit_damages, damage=ed.damage))

        return Event(EventType.ATTACK_HITS,
                     EventData(function=multi_hit_times, attacker=attacker, defender=defender,
                               damage=ed.damage))

    # TODO: refactor this into move class with an optional next-function which defaults to normal attack_hits
    def attack_hits_or_misses(event_data: "EventData"):
        # Check if attack hits
        r = random.randint(0, 100)
        if event_data.chance is None or event_data.chance > r:
            return multi_hit_hits(event_data)
        else:
            return [Event(EventType.ATTACK_MISSES,
                          EventData(lambda ed: []))]

    dmg = self.calculate_unmodified_damage(attacker, defender)
    return Event(EventType.ATTACK_TRIES_TO_HIT,
                 EventData(function=attack_hits_or_misses, defender=defender, attacker=attacker, damage=dmg,
                           chance=self.get_hit_chance(attacker, defender),
                           multiplier=type_multiplier(self.types, defender.types)
                           )
                 )





Sing = Move("Sing", 0, 55, PokemonType.NORMAL, MoveCategory.STATUS, effects=[MoveInflictSleep()])
Tackle = Move("Tackle", 40, 95, PokemonType.NORMAL, MoveCategory.PHYSICAL)
KarateChop = Move("Karate Chop", 50, 100, PokemonType.FIGHTING, MoveCategory.PHYSICAL, crit_chance=0.3)
DoubleSlap = Move("Double Slap", 15, 85, PokemonType.NORMAL, MoveCategory.PHYSICAL, use_function=multi_hit)
CometPunch = Move("Comet Punch", 18, 85, PokemonType.NORMAL, MoveCategory.PHYSICAL, use_function=multi_hit)
MegaPunch = Move("MegaPunch", 80, 85, PokemonType.NORMAL, MoveCategory.PHYSICAL)
PayDay = Move("PayDay", 40, 100, PokemonType.NORMAL, MoveCategory.PHYSICAL, False)  # TODO: Payday effect
FirePunch = Move("Fire Punch", 75, 100, PokemonType.FIRE, MoveCategory.PHYSICAL, effects=[MoveInflictBurnChance(10)])
Thunderbolt = Move("Thunderbolt", 90, 100, PokemonType.ELECTRIC, MoveCategory.SPECIAL, effects=[MoveInflictParalyzeChance(30)])
Takedown = Move("Takedown", 90, 85, PokemonType.NORMAL, MoveCategory.PHYSICAL, recoil_percent=25)


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