goals = [("alex","paris"),("jason","jfk"),("bill","montreal") ]

preconds = [("r1","london"), ("r2","london"),("r3","paris"), ('alex', 'London'),('jason', 'London'), ('bill', 'London') ,("has-fuel","r1"),("has-fuel","r2"),("has-fuel","r3")]


cargos = ["alex","jason","pencil","paper"]
rockets  = ["r1","r2"]
places = ["london","paris","jkf"]

initial_states = {
    "at":[("alex","london"),("jason","london"),("pencil","london"),("paper","london"), ("r1","london"),("r2","london")  ],
    "has_fuel":["r1","r2"],
    "in":[],
    "has_fuel_not":[],
    "in_not":[],
    "at_not":[]
}

resulting_states = initial_state

def load(a_cargo, a_rocket, a_place):
    if(cargo_in_rocket(a_cargo, a_rocket)):
        return False,None
    cargo_place = find_location(a_cargo)
    rocket_place = find_location(a_rocket)
    if(not cargo_place or not rocket_place or cargo_place != rocket_place):
        return False
    if(a_place != cargo_place):
        return False
    return True, (a_cargo, a_place)

actions = {
    "load": load,
    "unload": unload,
    "move":move
}

print(actions['loading']())


def find_location(a_cargo_or_a_place):
    for  index,tup in enumerate(initial_states["at"]):
        if isinstance(tup, tuple) and len(tup) == 2 and a_cargo_or_a_place == tup[0]:
            return tup[1]
    return None


def cargo_in_rocket(a_cargo, a_rocket):
    for index, tup in enumerate(initial_states["in"]):
        if isinstance(tup, tuple) and len(tup) == 2 and a_cargo == tup[0] and a_rocket == tup[1]:
            return True 
    return False
# Initial_state and goals 

# (preconds, eff)

'''









'''