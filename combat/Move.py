from typing import List
from combat.constants.move_effects import MoveEffect
from combat.constants.move_categories import MoveCategory
from combat.constants.pokemon_types import PokemonType
from Pokemon import Pokemon
from combat.event import Event, EventData, EventType
import random


class Move:
    def __init__(self, name: str, power: int, accuracy: int, pokemon_type: List[PokemonType],
                 category: MoveCategory, contact: bool, effects: List[MoveEffect], use_function=None,
                 recoil_percent=None, absorb_percent=None):
        self.__name = name
        self.__power = power
        self.__accuracy = accuracy
        self.__type = pokemon_type
        self.__category = category
        self.__contact = contact
        self.__effects = effects
        self.__recoil_percent = recoil_percent
        self.__absorb_percent = absorb_percent
        if use_function is None:
            self.__function = self.normal_use
        else:
            self.__function = use_function

    @staticmethod
    def simple_damage(data: EventData):
        data.defender.damage(data.damage)

    @staticmethod
    def damage_adds(self, damage: int, attacker: Pokemon, defender: Pokemon):
        events = []
        if self.recoil_percent is not None:
            events.append(Event(EventType.RECOIL_DAMAGE,
                                EventData(
                                    lambda event_data: self.simple_damage(event_data),
                                    defender=attacker, damage=damage * self.recoil_percent)
                                )
                          )

        if self.absorb_percent is not None:
            events.append(Event(EventType.ABSORB_HEALTH,
                                EventData(
                                    lambda event_data: self.simple_damage(event_data),
                                    defender=attacker, damage=-damage * self.absorb_percent)
                                )
                          )
        return events

    @staticmethod
    def normal_use(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
        def attack_hits_or_misses(event_data: "EventData"):
            r = random.randint(0, 100)
            if event_data.chance is None or event_data.chance > r:
                # Actually do the damage
                damage = event_data.defender.damage(event_data.damage)

                # Create events for possible other effects of the attack
                events = self.damage_adds(self, damage, attacker, defender)
                effect_events = list(map(lambda e: e.affect(attacker, defender, None), self.effects))
                for ev_l in effect_events:
                    events.extend(ev_l)
                return events
            else:
                return [Event(EventType.POKEMON_MISSES,
                              EventData(lambda ed: []))]

        dmg = self.calculate_damage(attacker, defender)
        attack_event = Event(EventType.POKEMON_ATTACKS,
                      EventData(
                                  attack_hits_or_misses,
                                  defender=defender, attacker=attacker, damage=dmg, chance=self.accuracy
                                )
                      )

        l = [attack_event]

        return l

    def use(self, attacker: Pokemon, defender: Pokemon) -> List[Event]:
        return self.__function(self, attacker, defender)

    def calculate_damage(self, attacker: Pokemon, defender: Pokemon):
        return 15
        # TODO: calculate damage

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

    def get_power(self):
        return self.__power

    @property
    def accuracy(self):
        return self.__accuracy

    def get_type(self):
        return self.__type

    def get_category(self):
        return self.__category

    def get_contact(self):
        return self.__contact

    def get_effects(self):
        return self.__effects
