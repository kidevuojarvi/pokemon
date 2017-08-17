from typing import List
from combat.constants.move_effects import MoveEffect
from combat.constants.move_categories import MoveCategory
from combat.constants.pokemon_types import PokemonType
from Pokemon import Pokemon
from combat.event import Event, EventData, EventType


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
    def normal_use(self, attacker: Pokemon, defender: Pokemon):
        dmg = self.__calculate_damage(attacker, defender)
        events = [Event(EventType.POKEMON_ATTACKS,
                        EventData(defendant=defender, attacker=attacker, defender_damage=dmg))]

        if self.__recoil_percent is not None:
            events.append(Event(EventType.RECOIL_DAMAGE,
                                EventData(attacker=attacker, attacker_damage=dmg * self.__recoil_percent)))

        if self.__absorb_percent is not None:
            events.append(Event(EventType.ABSORB_HEALTH,
                                EventData(attacker=attacker, attacker_damage=-dmg * self.__absorb_percent)))

        return events

    def use(self, attacker: Pokemon, defender: Pokemon) -> List[Event]:
        return self.__function(self, attacker, defender)

    def __calculate_damage(self, attacker: Pokemon, defender: Pokemon):
        return 15
        # TODO: calculate damage

    def get_name(self):
        return self.__name

    def get_power(self):
        return self.__power

    def get_accuracy(self):
        return self.__accuracy

    def get_type(self):
        return self.__type

    def get_category(self):
        return self.__category

    def get_contact(self):
        return self.__contact

    def get_effects(self):
        return self.__effects
