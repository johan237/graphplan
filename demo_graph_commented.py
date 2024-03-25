from collections import defaultdict

class GraphPlan:
    def __init__(self, operators, initial_state, goals):
        """
        Initialize the GraphPlan algorithm with operators, initial state, and goals.

        Parameters:
        operators (list): List of operators, each represented as a dictionary.
        initial_state (list): List of initial state predicates.
        goals (list): List of goal predicates.
        """
        self.operators = operators
        self.initial_state = initial_state
        self.goals = goals
        self.graph = defaultdict(list)
        self.solutions = []

    def expand_graph(self, level):
        """
        Expand the planning graph by applying applicable operators to the current level.

        Parameters:
        level (int): Current level in the planning graph.
        """
        self.graph[level] = self.graph[level - 1].copy()
        for operator in self.operators:
            if self.is_applicable(operator, level):
                self.apply_effects(operator, level)

    def is_applicable(self, operator, level):
        """
        Check if an operator is applicable at the given level.

        Parameters:
        operator (dict): Operator to check for applicability.
        level (int): Current level in the planning graph.

        Returns:
        bool: True if the operator is applicable, False otherwise.
        """
        preconditions = operator['preconds']
        for precondition in preconditions:
            if precondition not in self.graph[level][-1]:
                return False
        return True

    def apply_effects(self, operator, level):
        """
        Apply the effects of an operator to the current level of the planning graph.

        Parameters:
        operator (dict): Operator whose effects are to be applied.
        level (int): Current level in the planning graph.
        """
        effects = operator['effects']
        for effect in effects:
            if effect not in self.graph[level]:
                self.graph[level].append(effect)

    def extract_solution(self, level):
        """
        Extract the solution plan from the planning graph.

        Parameters:
        level (int): Level at which the solution is found.

        Returns:
        list: List of operators constituting the solution plan.
        """
        solution = []
        i = level - 1
        while i >= 0:
            for operator in self.operators:
                all_effects_present = True
                for effect in operator['effects']:
                    if effect not in self.graph[i][-1]:
                        all_effects_present = False
                        break
                if all_effects_present:
                    solution.append(operator)
                    i -= 1
                    break
        return solution[::-1]  # Reverse the path to obtain the optimal plan

    def save_solution_to_file(self, solution):
        """
        Save the solution plan to a text file.

        Parameters:
        solution (list): List of operators constituting the solution plan.
        """
        with open('plan.txt', 'w') as file:
            file.write("/*----------------------------------------------------------------------------*/\n")
            file.write("/* ------------------------           Final Plan      ------------------------*/\n")
            file.write("/*----------------------------------------------------------------------------*/\n\n")
            file.write("PLAN :\n\n")
            for operator in solution:
                operator_str = f"{operator['operator'][1]}_{operator['params'][1]}_{operator['params'][0]}_{operator['params'][2]}\n"
                file.write(operator_str)
            file.write("\n")
            """
            Save the solution plan to a text file.

            Parameters:
            solution (list): List of operators constituting the solution plan.
            """
            with open('plan.txt', 'w') as file:
                file.write("/*----------------------------------------------------------------------------*/\n")
                file.write("/* ------------------------           Final Plan      ------------------------*/\n")
                file.write("/*----------------------------------------------------------------------------*/\n\n")
                file.write("PLAN :\n\n")
                for operator in solution:
                    params = operator['params']
                    file.write(f"{operator['operator']}_{params[1]}_{params[0]}_{params[2]}\n")
                file.write("\n")

    def plan(self):
        """
        Execute the GraphPlan algorithm to find a solution plan.
        """
        self.graph[0].append(self.initial_state)
        self.graph[0].append(self.goals)
        level = 1
        while True:
            for i in range(level):
                if all(goal in self.graph[i][-1] for goal in self.goals):
                    solution = self.extract_solution(i)
                    self.save_solution_to_file(solution)  # Save the solution to a file
                    self.solutions.append(solution)
                    return self.solutions
            self.expand_graph(level)
            level += 1

def parse_file(filename):
    """
    Parse a file and return its contents as a list of lines.

    Parameters:
    filename (str): Name of the file to parse.

    Returns:
    list: List containing the lines of the file.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    items = [line.strip() for line in lines if line.strip()]
    return items

def parse_operators(ops_file):
    """
    Parse operator definitions from a file and return them as a list of dictionaries.

    Parameters:
    ops_file (file): File containing operator definitions.

    Returns:
    list: List of dictionaries representing operators.
    """
    operators = []
    current_operator = {}
    for line in ops_file:
        if line.startswith('(operator'):
            if current_operator:
                operators.append(current_operator)
            current_operator = {'operator': '', 'params': [], 'preconds': [], 'effects': []}
            current_operator['operator'] = line.split()
        elif line.startswith('('):
            parts = line.strip('()').split()
            if parts[0] == 'params':
                current_operator['params'] = parts[1:]
            elif parts[0] == 'preconds':
                current_operator['preconds'].append(tuple(parts[1:]))
            elif parts[0] == 'effects':
                current_operator['effects'].append(tuple(parts[1:]))
    if current_operator:
        operators.append(current_operator)
    print(operators)
    return operators

def parse_facts(facts_file):
    """
    Parse facts from a file and return them as preconditions and effects.

    Parameters:
    facts_file (file): File containing facts.

    Returns:
    dict: Dictionary containing preconditions and effects.
    """
    facts = {'preconds': [], 'effects': []}
    current_section = 'preconds'
    for line in facts_file:
        if line.startswith('(effects'):
            current_section = 'effects'
        elif line.startswith('('):
            facts[current_section].append(tuple(line.strip('()').split()[1:]))
    print(facts)
    return facts

def DoPlan(ops_file, facts_file):
    """
    Execute the planning process.

    Parameters:
    ops_file (file): File containing operator definitions.
    facts_file (file): File containing facts.

    Returns:
    list: List of solutions if found, otherwise an empty list.
    """
    operators = parse_operators(ops_file)
    facts = parse_facts(facts_file)
    initial_state = facts['preconds']
    goals = facts['effects']
    planner = GraphPlan(operators, initial_state, goals)
    solutions = planner.plan()
    if solutions:
        for solution in solutions:
            print("Solution:")
            for operator in solution:
                print(operator)
            print()
    else:
        print("No solution found.")

# Example usage
if __name__ == "__main__":
    with open('./Exemples/r_ops.txt', 'r') as ops_file:
        ops_content = ops_file.readlines()
    with open('./Exemples/r_fact3.txt', 'r') as facts_file:
        facts_content = facts_file.readlines()

    DoPlan(ops_content, facts_content)
