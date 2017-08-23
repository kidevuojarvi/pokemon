from typing import List
from combat.constants.move_effects import MoveEffect
from combat.constants.move_categories import MoveCategory
from combat.constants.pokemon_types import PokemonType
from Pokemon import Pokemon
from combat.event import Event, EventData, EventType
from random import randint
from combat.util.util import flatten_events
from combat.constants.pokemon_types import type_multiplier


class Move:
    def __init__(self, name: str, power: int, accuracy: int, types,
                 category: MoveCategory, contact: bool = None, effects: List[MoveEffect]=None, use_function=None,
                 recoil_percent=None, absorb_percent=None, crit_chance=None):
        self.__name = name
        self.__power = power
        self.__accuracy = accuracy
        self.__types = types if isinstance(types, list) else [types]
        self.__category = category
        self.__contact = contact if contact is not None else True if category == MoveCategory.PHYSICAL else False
        self.__effects = effects if effects is not None else list()
        self.__recoil_percent = recoil_percent
        self.__absorb_percent = absorb_percent
        if use_function is None:
            self.__function = self.normal_use
        else:
            self.__function = use_function
        self.__crit_chance = crit_chance if crit_chance is not None else 10  # TODO: real crit chance?

    @staticmethod
    def absorb_health(data: EventData):
        healed = data.defender.heal(data.damage)
        if healed > 0:
            return Event(EventType.FINAL_HEALTH_ABSORBED,
                         EventData(defender=data.defender, damage=healed, move=data.move))

    @staticmethod
    def recoil_damage(data: EventData):
        took = data.defender.damage(data.damage)
        if took > 0:
            return Event(EventType.FINAL_TOOK_RECOIL_DAMAGE,
                         EventData(defender=data.defender, damage=took, move=data.move))

    @staticmethod
    def damage_adds(self, damage: int, attacker: "Pokemon"):
        events = []
        if self.recoil_percent is not None:
            events.append(Event(EventType.RECOIL_DAMAGE,
                                EventData(
                                    function=self.recoil_damage, move=self,
                                    defender=attacker, damage=damage * self.recoil_percent,)
                                )
                          )

        if self.absorb_percent is not None:
            events.append(Event(EventType.ABSORB_HEALTH,
                                EventData(
                                    function=self.absorb_health, move=self,
                                    defender=attacker, damage=damage * self.absorb_percent)
                                )
                          )
        return events

    @staticmethod
    def attack_hits(event_data: "EventData"):
        def attackhits(e_d: "EventData"):
            # If the move does damage
            if e_d.damage is None or e_d.damage > 0:
                # Actually do the damage
                potential_dmg, critical = event_data.move.calculate_real_damage_with_crit(e_d)
                damage = e_d.defender.damage(potential_dmg)
                events = [Event(EventType.FINAL_ATTACK_DID_DAMAGE, EventData(damage=e_d.damage, defender=e_d.defender, move=e_d.move))]
                if critical:
                    events.append(Event(EventType.FINAL_ATTACK_CRIT,
                                        EventData(damage=damage, attacker=e_d.attacker, defender=e_d.defender, move=e_d.move)))
                # Create events for possible other effects of the attack (absorb, recoil, status chances, ...)
                events.extend(e_d.move.damage_adds(e_d.move, damage, e_d.attacker))
            else:
                events = []

            effect_events = list(map(lambda e: e.affect(e_d.attacker, e_d.defender, None), e_d.move.effects))
            for ev_l in effect_events:
                events.extend(flatten_events(ev_l))
            return events

        return Event(EventType.ATTACK_HITS,
                     EventData(function=attackhits, defender=event_data.defender, attacker=event_data.attacker,
                               damage=event_data.damage, multiplier=event_data.multiplier, move=event_data.move,
                               crit_chance=event_data.move.crit_chance))

    @staticmethod
    def attack_hits_or_misses(event_data: "EventData", hit_function=None):
        """
        :param event_data:
        :param hit_function: Optional custom hit function. Calls normal hit function if not given
        :return:
        """

        r = randint(0, 100)
        if event_data.chance is None or event_data.chance > r:
            if hit_function is None:
                return Move.attack_hits(event_data)
            else:
                return hit_function(event_data)
        else:
            return Event(EventType.FINAL_ATTACK_MISSES,
                         EventData(defender=event_data.defender, attacker=event_data.attacker, move=event_data.move))

    @staticmethod
    def normal_use(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
        dmg = self.calculate_unmodified_damage(attacker, defender)
        attack_event = Event(EventType.ATTACK_TRIES_TO_HIT,
                             EventData(
                                  self.attack_hits_or_misses,
                                  defender=defender, attacker=attacker, damage=dmg, move=self,
                                  chance=self.get_hit_chance(attacker, defender),
                                  multiplier=type_multiplier(self.__types, defender.types)
                                  )
                             )

        return attack_event

    @staticmethod
    def multi_hit(self: "Move", attacker: "Pokemon", defender: "Pokemon"):
        def multi_hit_hits(ed: "EventData"):
            def multi_hit_times(ed: "EventData"):
                def multi_hit_damages(ed: "EventData"):
                    return [self.attack_hits(ed) for _ in range(ed.multiplier)]
                r = randint(0, 5)
                times = [2, 2, 3, 3, 4, 5][r]
                return Event(EventType.MULTI_HIT_TIMES,
                             EventData(multiplier=times, attacker=attacker, defender=defender,
                                       function=multi_hit_damages, damage=ed.damage, move=ed.move))

            return Event(EventType.ATTACK_HITS,
                         EventData(function=multi_hit_times, attacker=attacker, defender=defender,
                                   damage=ed.damage, move=ed.move))

        dmg = self.calculate_unmodified_damage(attacker, defender)
        return Event(EventType.ATTACK_TRIES_TO_HIT,
                     EventData(function=lambda ed: Move.attack_hits_or_misses(ed, multi_hit_hits),
                               defender=defender, attacker=attacker, damage=dmg,
                               chance=self.get_hit_chance(attacker, defender), move=self,
                               multiplier=type_multiplier(self.types, defender.types)
                               )
                     )

    @staticmethod
    def calculate_real_damage_with_crit(event_data: "EventData"):
        r = randint(0, 100)
        base = event_data.damage
        multiplied = base * event_data.multiplier
        crit = event_data.crit_chance is not None and r < event_data.crit_chance
        critted = multiplied * 2 if crit else multiplied  # TODO: crit damage calculation
        return critted, crit

    def get_hit_chance(self, attacker: "Pokemon", defender: "Pokemon"):
        # TODO: use accuracy and evasion modifiers
        return self.accuracy

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

    @property
    def name(self):
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

    @property
    def crit_chance(self):
        return self.__crit_chance


class MoveFunctions:
    multi_hit = Move.multi_hit
