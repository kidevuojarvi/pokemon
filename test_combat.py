from Pokemon import Pokemon
from combat.implementations.move_list import *
from combat.event import Event
from typing import List
from combat.util.util import flatten_events

if __name__ == "__main__":
    pokemon1 = Pokemon(1, 50)
    pokemon2 = Pokemon(4, 50)

    e = flatten_events(Imagine.use(pokemon1, pokemon2))

    for i in e:
        print(i.type)
        e.extend(flatten_events(i.call()))




