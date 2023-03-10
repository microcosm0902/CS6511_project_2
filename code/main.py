'''
This program implements the CSP algorithm to solve this coloring problem. The CSP algorithm has the following
components:
•  Search algorithm to solve the CSP
•  Heuristics (min remaining values, least constraining value)
•  Constraint propagation using AC3
The input format is specified in the project document.
'''

class CSP:
    def __init__(self, file_path):
        self.read_file(file_path)

    '''
    read the file, initialize variables, constrains, domains and the graph
    '''
    def read_file(self, file_path):
        constraints = set()
        self.graph = {}
        with open(file_path) as f:
            for line in f:
                if "colors" in line:
                    self.colors = int(line.split("=")[1].strip())
                elif line[0] == "#":
                    continue
                else:
                    ws = line.split(",")
                    if len(ws) != 2:
                        continue
                    x = int(ws[0])
                    y = int(ws[1])
                    constraints.add((x, y))
                    constraints.add((y, x))
                    if x not in self.graph:
                        self.graph[x] = set()
                    self.graph[x].add(y)
                    if y not in self.graph:
                        self.graph[y] = set()
                    self.graph[y].add(x)
        self.constrains = list(constraints)
        self.variables = set([i[0] for i in self.constrains])
        self.domains = {}
        for i in self.variables:
            self.domains[i] = set(range(self.colors))

    # implement AC3
    def AC3(self, constrains, domains):
        q = constrains.copy()
        while len(q) > 0:
            arc = q.pop()
            while True:
                flag = False
                to_remove = []
                for i in domains[arc[0]]:
                    incons = True
                    for j in domains[arc[1]]:
                        if i != j:
                            incons = False
                            break
                    if incons:
                        to_remove.append(i)
                        # domains[arc[0]].remove(i)
                        flag = True
                        for k in constrains:
                            if i == k[1]:
                                if k not in q:
                                    q.append(k)

                if len(to_remove) > 0:
                    flag = True
                    for i in to_remove:
                        domains[arc[0]].remove(i)
                if not flag:
                    break

   # implements min remaining value heuristic
    def min_remaining_value(self, coloring, variables, domains):
        domains = [(i, domains[i]) for i in variables]
        domains.sort(key=lambda x: len(x[1]))
        return [x[0] for x in domains if x[0] not in coloring]

    # implements most constrained heuristic
    def most_constrained(self, variables, graph):
        graph = [(i, graph[i]) for i in variables]
        graph.sort(key=lambda x: -len(x[1]))
        max_len = len(graph[0][1])
        return [x[0] for x in graph if len(x[1]) == max_len]

    # implements the least constraining value heuristic
    def least_constraining_values(self, var, domains,graph):
        least_rule_out = float("inf")
        value_rule_out = {}
        for i in domains[var]:
            rule_out = 0
            for j in graph[var]:
                for k in domains[j]:
                    if k == i:
                        rule_out += 1
            if rule_out < least_rule_out:
                least_rule_out = rule_out
            value_rule_out[i] = rule_out
        items = list(value_rule_out.items())
        items.sort(key=lambda x: x[1])
        return [i[0] for i in items]

    # fast fail if no valid value for a variable
    def fast_fail(self, domains):
        for i in domains:
            if len(domains[i]) == 0:
                return True
        return False

    # perform backtracking
    def search(self, coloring, graph, domains, constrains, variables):
        if len(coloring) == len(self.variables):
            return True
        self.AC3(constrains, domains)
        if self.fast_fail(domains):
            return False

        min_remaining_value_variables = self.min_remaining_value(coloring, variables, domains)
        most_constrained_variables = self.most_constrained(min_remaining_value_variables, graph)
        values_sorted = self.least_constraining_values(most_constrained_variables[0], domains, graph)
        var = most_constrained_variables[0]
        next_domain = domains.copy()

        for i in values_sorted:
            coloring[var] = i
            next_domain[var] = [i]
            if self.search(coloring, graph, next_domain, constrains, variables):
                return True
            del coloring[var]
        return False

    # just call search to get back the result
    def solve(self):
        coloring = {}
        if self.search(coloring, self.graph, self.domains, self.constrains, self.variables):
            return coloring
        else:
            return {}

    # present the solution
    def present(self, coloring):
        if len(coloring) > 0:
            print("coloring scheme found!")
            for i in coloring:
                print(f"vertex: {i} color: {coloring[i]}")
        else:
            print("No coloring is possible")


# usage python main.py <path_to_test_file>
if __name__ == "__main__":
    import sys
    csp = CSP(sys.argv[1])
    coloring = csp.solve()
    csp.present(coloring)