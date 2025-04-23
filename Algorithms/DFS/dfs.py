import time

# Pop value from the stack and insert into visited
# Add new neighbours into stack
# But if visited then ignore above
# Repeat until goal is found
def dfs(start, goal, graph):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()  # pop the last item
        graph.current = node

        if node in visited: continue

        visited.add(node)
        node.visited = True
        if node == goal:
            graph.graph_update(node, True)
            return

        for neighbour, weight in graph.graph.get_neighbours(node):
            if neighbour in visited or neighbour.obstacle: # skip walls
              continue

            neighbour.expanded = True
            neighbour.g_cost = node.g_cost + weight
            neighbour.parent = node
            stack.append(neighbour)

        graph.graph_update(node)
        time.sleep(graph.delay)

    print("No path")


def dfs_tree(start, goal, graph):
    stack = [start]

    while stack:
        node = stack.pop()  # pop the last item
        graph.current = node

        node.visited = True
        if node == goal:
            graph.graph_update(node, True)
            return

        for neighbour, weight in graph.graph.get_neighbours(node):
            if neighbour == node.parent or neighbour.obstacle: # skip walls
              continue

            neighbour.expanded = True
            neighbour.g_cost = node.g_cost + weight
            neighbour.parent = node
            stack.append(neighbour)

        graph.graph_update(node)
        time.sleep(graph.delay)

    print("No path")
