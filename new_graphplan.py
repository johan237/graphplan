cargos = ["alex","jason","bill"]
rockets  = ["r1","r2","r3"]
places = ["london","paris","jfk","montreal"]
goals = [("alex","paris"),("jason","jfk") ,("bill","montreal")]

preconds = [("r1","london"), ("r2","london"),("r3","paris"), ('alex', 'london'),('jason', 'london'), ('bill', 'london') ,("has-fuel","r1"),("has-fuel","r2"),("has-fuel","r3")]

initial_states = {
    "at":[("alex","london"),("jason","london"),("bill","london"),("r3","paris"), ("r1","london"),("r2","london")  ],
    "has_fuel":["r1","r2","r3"],
    "in":[],
    "has_fuel_not":[],
    "in_not":[],
    "at_not":[]
}

action_state = {
    0:{ 
        "load": {
                 "preconds":{
                     "at":["id_1","id_2"],
                 },
                 "effects":{
                     "at_not":["id_1","id_2","id_3"],
                     "in":["id_1"]
                 }
                 },
        "unload": {
                 "preconds":{
                     "at":["id_1","id_2"],
                     "in":["id_2"]
                 },
                 "effects":{
                     "at":["id_1","id_2","id_3"],
                     "in_not":["id_1"]
                 }
                 },
        "move": {
                 "preconds":{
                     "at":["id_1","id_2"],
                     "has_fuel":["id_2"]
                 },
                 "effects":{
                     "at":["id_1","id_2","id_3"],
                     "has_fuel_not":["id_1"],
                     "at_not":["id_1"]
                 }
                 }    
    }
}


def generate_pairs(array):
    pairs = []
    for i in range(len(array)):
        for j in range(i+1, len(array)):
            pairs.append((array[i], array[j]))
            pairs.append((array[j], array[i]))
    return pairs
class Graphplan:
    def __init__(self,cargos,rockets,places,preconds,goals,initial_states):
        self.cargos = cargos
        self.rockets =rockets
        self.places =places
        self.preconds = preconds
        self.goals = goals
        self.initial_states = initial_states
        self.level = 0
        self.graph = {0: initial_states}
        self.pairs = generate_pairs(places)
        
    def check_goals(self):
        for goal in self.goals:
            found = False
            for state in self.graph[self.level]["at"]:
                if goal == state:
                    found = True
            if not found:
                return False
        return True
    
    def execute(self):
        while True:
            print("Executing")
            print(self.graph[self.level]["at"])
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx   ")
            print(" ")
            if(self.check_goals()):
                print("Goals Found.........................xxxxxxxxxx")
                break
            else:
                print("Goals Not Found.....................Continuing")
            if self.level == 5:
                break
            global current_state
            current_state = self.graph[self.level]
            for cargo in self.cargos:
                for rocket in self.rockets:
                    for place in self.places:
                        load(cargo,rocket,place)
                        unload(cargo,rocket,place)

            for rocket in self.rockets:
                for from_place, to_place in self.pairs:
                    move(rocket,from_place, to_place)
            
            self.level = self.level+1
            self.graph[self.level] = current_state
    
    def extract_solution(self):
        return 0


def append_if_not_in(where_to_append, element):
    try:
        index = where_to_append.index(element)
        return index
    except ValueError:  # item not found in the list
        where_to_append.append(item)
        return len(where_to_append) - 1
    

def load(a_cargo, a_rocket, a_place):
    if(not is_in_place(a_cargo, a_place) or not is_in_place(a_rocket, a_place)):
        return False, None
    append_if_not(current_state["in"],(a_cargo, a_rocket))
    append_if_not(current_state["at_not"],(a_cargo, a_place))
    # TODO: retrieve indices and put inside state action pair
    return True, (a_cargo, a_place)


def unload(a_cargo, a_rocket, a_place):
    if(not is_in_place(a_rocket,a_place)):
        return False, None
    if(not cargo_is_in_rocket(a_cargo, a_rocket)):
        return False, None
    append_if_not(current_state["at"],(a_cargo, a_place))
    append_if_not(current_state["in_not"],(a_cargo, a_rocket))
    
def move( a_rocket,from_place, to_place):
    if( not has_fuel(a_rocket)):
        return False, None
    if( not is_in_place(a_rocket, from_place)):
        return False, None

    append_if_not(current_state["at"],(a_rocket, to_place))
    append_if_not(current_state["at_not"],(a_rocket, from_place))
    append_if_not(current_state["has_fuel_not"],a_rocket)



actions = {
    "load": load,
    "unload": unload,
    "move":move
}

def has_fuel(a_plane):
    for plane in initial_states["has_fuel"]:
        if plane == a_plane:
            return True
    return False

def is_in_place(a_cargo_or_a_plane, location):
    for  index,tup in enumerate(initial_states["at"]):
        if isinstance(tup, tuple) and len(tup) == 2 and (a_cargo_or_a_plane,location) == tup:
            return True
    return False


def cargo_is_in_rocket(a_cargo, a_rocket):
    for index, tup in enumerate(initial_states["in"]):
        if isinstance(tup, tuple) and len(tup) == 2 and a_cargo == tup[0] and a_rocket == tup[1]:
            return True 
    return False


graphplan  = Graphplan(cargos,rockets,places,preconds,goals,initial_states)

graphplan.execute()