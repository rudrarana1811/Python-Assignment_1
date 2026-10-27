import heapq


def add_dependency(graph, dependency_count, module, dependency):
    if dependency not in graph[module]:
        graph[module].add(dependency)
        dependency_count[module] += 1


def find_cycle(graph):
    state = {}
    path = []
    position = {}
    cycle = []
# DFS is used only to report one cycle
    def visit(module):
        state[module] = 1
        position[module] = len(path)
        path.append(module)

        for dependency in sorted(graph[module]):
            if state.get(dependency, 0) == 0:
                if visit(dependency):
                    return True

            elif state.get(dependency) == 1:
                start = position[dependency]
                cycle.extend(path[start:])
                cycle.append(dependency)
                return True

        path.pop()
        position.pop(module, None)
        state[module] = 2
        return False

    for module in sorted(graph):
        if state.get(module, 0) == 0:
            if visit(module):
                return cycle

    return []


print("Python Module Dependency Resolver")
print("Enter number of modules and import relationships:")
n, e = map(int, input().split())

modules = []
graph = {}
dependency_count = {}

print("Enter module names:")

for i in range(n):
    print(f"Module {i + 1}:")
    module = input().strip()

    modules.append(module)
    graph[module] = set()
    dependency_count[module] = 0

print("Enter import relationships:")
print("Format: module_a imports module_b")

for i in range(e):
    print(f"Relationship {i + 1}:")
    module, dependency = input().split()

    if module not in graph or dependency not in graph:
        print("Invalid module name")
        raise SystemExit

    add_dependency(
        graph,
        dependency_count,
        module,
        dependency
    )

ready = []

for module in modules:
    if dependency_count[module] == 0:
        heapq.heappush(ready, module)

order = []

while ready:
    module = heapq.heappop(ready)
    order.append(module)

    for other in sorted(graph):
        if module in graph[other]:
            dependency_count[other] -= 1

            if dependency_count[other] == 0:
                heapq.heappush(ready, other)

if len(order) == n:
    print()
    print(*order)
else:
    cycle = find_cycle(graph)
    print("CYCLE", *cycle)
