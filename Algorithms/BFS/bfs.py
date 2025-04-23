import time

# Pop value from the queue and insert into visited
# Add new neighbours into queue
# But if visited then ignore above
# Repeat until goal is found

# BFS can only be used to find shortest path in a graph if
# There are no loops and all edges have same weight or no weight.
def bfs(start, goal, graph):
    # if a node has been visited
    # its neighbours have been expanded
    visited = set() # nodes that have been visited
    queue = [start] # nodes to explore

    while queue: # while there are nodes to explore
        node = queue.pop(0) # pop the first item (queue FIFO)
        graph.current = node 

        # if node is in visited its
        # neighbours have already been checked
        if node in visited: continue

        visited.add(node)
        node.visited = True
        if node == goal: # found goal
            graph.graph_update(node, True)
            return
        
        # get neighbouring nodes
        for neighbour, weight in graph.graph.get_neighbours(node):
            if neighbour in visited or neighbour.obstacle: # skip visited or osbtacles
              continue 

            # for visualiser
            neighbour.expanded = True
            neighbour.g_cost = node.g_cost + weight

            neighbour.parent = node # reconstructing the path
            queue.append(neighbour) # if a neighbour isnt visited, add it

        graph.graph_update(node)
        time.sleep(graph.delay)

    print("No path")

def bfs_tree(start, goal, graph):
    # if a node has been visited
    # its neighbours have been expanded
    queue = [start]

    while queue:
        node = queue.pop(0) # pop the first item
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
            queue.append(neighbour)

        graph.graph_update(node)
        time.sleep(graph.delay)

    print("No path")
