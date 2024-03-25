# Define State class to represent the state of cargos and airplanes
class State:
    def __init__(self, cargos, airplanes):
        self.cargos = cargos  # List of tuples (cargo_id, current_location)
        self.airplanes = airplanes  # List of tuples (airplane_id, current_location, cargo_list)

# Define Action class to represent the movement of cargos
class Action:
    def __init__(self, preconditions, postconditions):
        self.preconditions = preconditions  # List of tuples (cargo_id, current_location)
        self.postconditions = postconditions  # List of tuples (cargo_id, destination)

# Define GraphPlan algorithm
def graphplan(initial_state, goal_state, actions):
    level = 0
    graph = {0: [initial_state]}  # Graph to store levels and states

    while True:
        # Expand the graph with new level
        graph[level + 1] = []

        # Propagate actions backward
        actions_layer = []
        for action in actions:
            # Check if action's preconditions are satisfied
            if all(precondition in graph[level][-1].cargos for precondition in action.preconditions):
                actions_layer.append(action)
        
        for action in actions_layer:
            # Apply actions to create new states
            new_states = apply_action(action, graph[level][-1])
            for state in new_states:
                if state not in graph[level + 1]:
                    graph[level + 1].append(state)

        # Check for goal satisfaction
        if goal_state in graph[level + 1]:
            return extract_solution(graph, goal_state)

        # Check for deadlock
        if graph[level] == graph[level + 1]:
            return "No solution found"

        level += 1

# Define function to apply action to a state
def apply_action(action, state):
    new_states = []
    for cargo_id, _ in action.preconditions:
        # Remove cargos that are moved
        new_cargos = [(cargo[0], action.postconditions[i][1]) if cargo[0] == cargo_id else cargo for i, cargo in enumerate(state.cargos)]
        new_state = State(new_cargos, state.airplanes)
        new_states.append(new_state)
    return new_states

# Define function to extract solution from the graph
def extract_solution(graph, goal_state):
    solution = []
    level = len(graph) - 1
    current_state = goal_state
    while level >= 0:
        solution.insert(0, current_state)
        for state in graph[level]:
            if current_state in [s for s in apply_action(action, state) for action in actions]:
                current_state = state
                break
        level -= 1
    return solution

# Example usage
initial_state = State([(1, 'A'), (2, 'B')], [(1, 'A', [1]), (2, 'C', [2])])
goal_state = State([(1, 'B'), (2, 'A')], [(1, 'B', [1]), (2, 'A', [2])])
actions = [
    Action([(1, 'A')], [(1, 'B')]),
    Action([(2, 'C')], [(2, 'A')])
]

solution = graphplan(initial_state, goal_state, actions)
print(solution)
