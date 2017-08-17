from Pokemon import Pokemon
from combat.implementations.move_list import Tackle, Sing, Thunderbolt
from combat.event import Event

if __name__ == "__main__":
    pokemon1 = Pokemon(1, 50)
    pokemon2 = Pokemon(4, 50)

    event_q = []

    e = Thunderbolt.use(pokemon1, pokemon2)
    for i in e:
        print(i.type)
        e.extend(i.call())




