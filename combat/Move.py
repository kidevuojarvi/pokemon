from typing import List
from combat.constants.move_effects import MoveEffect
from combat.constants.move_categories import MoveCategory
from combat.constants.pokemon_types import PokemonType
from Pokemon import Pokemon
from combat.event import Event, EventData, EventType
import random
from combat.util.util import flatten_events
from combat.constants.pokemon_types import type_multiplier


class Move:
    def __init__(self, name: str, power: int, accuracy: int, elemental_types: List[PokemonType],
                 category: MoveCategory, contact: bool, effects: List[MoveEffect]=None, use_function=None,
                 recoil_percent=None, absorb_percent=None, crit_chance=None):
        self.__name = name
        self.__power = power
        self.__accuracy = accuracy
        self.__types = elemental_types
        self.__category = category
        self.__contact = contact
        self.__effects = effects if effects is not None else list()
        self.__recoil_percent = recoil_percent
        self.__absorb_percent = absorb_percent
        if use_function is None:
            self.__function = self.normal_use
        else:
            self.__function = use_function
        self.__crit_chance = crit_chance if crit_chance is not None else 0.1  # TODO: real crit chance?

    @staticmethod
    def simple_damage(data: EventData):
        data.defender.damage(data.damage)

    @staticmethod
    def absorb_health(data: EventData):
        healed = data.defender.heal(data.damage)
        if healed > 0:
            return Event(EventType.FINAL_HEALTH_ABSORBED,
                         EventData(lambda ed: [], defender=data.defender, damage=healed))

    @staticmethod
    def recoil_damage(data: EventData):
        took = data.defender.damage(data.damage)
        if took > 0:
            return Event(EventType.FINAL_TOOK_RECOIL_DAMAGE,
                         EventData(defender=data.defender, damage=took))

    @staticmethod
    def damage_adds(self, damage: int, attacker: "Pokemon"):
        events = []
        if self.recoil_percent is not None:
            events.append(Event(EventType.RECOIL_DAMAGE,
                                EventData(
                                    self.recoil_damage,
                                    defender=attacker, damage=damage * self.recoil_percent)
                                )
                          )

        if self.absorb_percent is not None:
            events.append(Event(EventType.ABSORB_HEALTH,
                                EventData(
                                    self.absorb_health,
                                    defender=attacker, damage=damage * self.absorb_percent)
                                )
                          )
        return events

    @staticmethod
    def normal_use(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
        def attack_hits_or_misses(event_data: "EventData"):
            # Check if attack hits
            r = random.randint(0, 100)
            if event_data.chance is None or event_data.chance > r:
                # If the move does damage
                if event_data.damage is None or event_data.damage > 0:
                    # Actually do the damage
                    potential_dmg, critical = self.calculate_real_damage(event_data, attacker, defender)
                    damage = event_data.defender.damage(potential_dmg)
                    events = [Event(EventType.FINAL_ATTACK_DID_DAMAGE, EventData(damage=event_data.damage, defender=defender))]
                    if critical:
                        events.append(Event(EventType.FINAL_ATTACK_CRIT,
                                            EventData(damage=damage, attacker=attacker, defender=defender)))
                    # Create events for possible other effects of the attack (absorb, recoil, status chances, ...)
                    events.extend(self.damage_adds(self, damage, attacker))
                else:
                    events = []

                effect_events = list(map(lambda e: e.affect(attacker, defender, None), self.effects))
                for ev_l in effect_events:
                    events.extend(flatten_events(ev_l))
                return events
            else:
                return [Event(EventType.POKEMON_MISSES,
                              EventData(lambda ed: []))]

        dmg = self.calculate_unmodified_damage(attacker, defender)
        attack_event = Event(EventType.POKEMON_ATTACKS,
                             EventData(
                                  attack_hits_or_misses,
                                  defender=defender, attacker=attacker, damage=dmg,
                                  chance=self.get_hit_chance(attacker, defender),
                                  multiplier=type_multiplier(self.__types, defender.types)
                                  )
                             )

        l = [attack_event]

        return l

    def get_hit_chance(self, attacker: "Pokemon", defender: "Pokemon"):
        # TODO: use accuracy and evasion modifiers
        return self.accuracy

    @staticmethod
    def calculate_real_damage(event_data: "EventData", attacker: "Pokemon", defender: "Pokemon"):
        r = random.randint(0, 100)
        base = event_data.damage
        multiplied = base * event_data.multiplier
        crit = event_data.crit_chance is not None and r < event_data.crit_chance
        critted = multiplied * 2 if crit else multiplied  # TODO: crit damage calculation
        return critted

    def use(self, attacker: Pokemon, defender: Pokemon) -> List[Event]:
        return self.__function(self, attacker, defender)

    def calculate_unmodified_damage(self, attacker: Pokemon, defender: Pokemon):
        # TODO: calculate damage
        return self.power

    @property
    def recoil_percent(self):
        return self.__recoil_percent

    @property
    def absorb_percent(self):
        return self.__absorb_percent

    @property
    def effects(self):
        return self.__effects

    def get_name(self):
        return self.__name

    @property
    def power(self):
        return self.__power

    @property
    def accuracy(self):
        return self.__accuracy

    @property
    def types(self):
        return self.__types

    @property
    def category(self):
        return self.__category

    @property
    def contact(self):
        return self.__contact

    @property
    def effects(self):
        return self.__effects
