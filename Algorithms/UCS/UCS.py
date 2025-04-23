from Algorithms.PriorityQueue import MinHeap

import time

# Priority Queue: UCS uses a priority queue to always explore the node with the lowest known cost.
# Cost Calculation: The cost of reaching a node (g_cost) is accumulated as the algorithm progresses.
# It starts from the source node with a cost of 0 and increments as it moves through the graph.
# Visited Nodes: To prevent revisiting nodes and to ensure optimality, the algorithm maintains a set of visited nodes.
# Goal State(s): UCS can handle multiple goal states. The algorithm continues until all goal states are reached.
def uniform_cost_search(start, goal, graph):
    # map to store visited node
    visited = set()
    # insert the starting index
    start.cost = 0
    heap = MinHeap([(start.cost, start)]) # uses our priority queue

    while heap.size > 0:
        # get the top element of the queue
        (cost, node) = heap.pop()
        graph.current = node

        if node in visited: continue

        visited.add(node)
        node.visited = True
        # if the node is the goal
        if node == goal:
            graph.graph_update(node, True)
            return

        # check for the non-visited nodes
        # which are adjacent to the present node
        for (neighbour, weight) in graph.graph.get_neighbours(node):
            if neighbour in visited or neighbour.obstacle: # skip walls
                continue

            # visualiser
            neighbour.expanded = True
            
            new_cost = node.cost + weight
            # A more optimal path to this neighbor has been found
            if new_cost < neighbour.cost:
                neighbour.cost = new_cost
                neighbour.parent = node # visual
                heap.push((neighbour.cost, neighbour))

        graph.graph_update(node)
        time.sleep(graph.delay)
        
    print("No path")

def uniform_cost_search_tree(start, goal, graph):
    # insert the starting index
    start.cost = 0
    heap = MinHeap([(start.cost, start)])

    while heap.size > 0:
        # get the top element of the queue
        (cost, node) = heap.pop()
        graph.current = node

        node.visited = True
        # if the node is the goal
        if node == goal:
            graph.graph_update(node, True)
            return

        # check for the non-visited nodes
        # which are adjacent to the present node
        for (neighbour, weight) in graph.graph.get_neighbours(node):
            if neighbour.obstacle: # skip walls
                continue

            neighbour.expanded = True
            new_cost = node.cost + weight
            # A more optimal path to this neighbor has been found
            if new_cost < neighbour.cost:
                neighbour.cost = new_cost
                neighbour.parent = node
                heap.push((neighbour.cost, neighbour))

        graph.graph_update(node)
        time.sleep(graph.delay)
        
    print("No path")