from Pokemon import Pokemon
from combat.constants.status_effects import StatusEffect

class EventType:
    pass

class StatusEvent(EventType):
    def __init__(self, affected: Pokemon, status_effect: StatusEffect):
        pass
        # TODO: do something with status effect