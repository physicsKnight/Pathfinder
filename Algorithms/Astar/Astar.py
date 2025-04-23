from Algorithms.PriorityQueue import MinHeap
from math import sqrt, ceil
import time

# admissibility: h_cost <= g_cost to goal
# consistency: 1: h(A) - h(C) <= g_cost(A to C)
#              2: TI: h(A) <= g_cost(A to C) + h(C)

# same as UCS but traverse in the direction
# of the lowest f_cost rather than g_cost
# g_cost is the same as cost in UCS
# h_cost is calculated by heuristic, which is
# the estimated cost from the current node to goal
# f_cost = g_cost + h_cost, total estimated cost

def astar(start, goal, graph):
    visited = set()
    start.f_cost = start.h_cost = heuristic(start, goal)
    # heap is ordered by f_cost rather than g_cost
    heap = MinHeap([(start.f_cost, start)])

    while heap.size > 0:
      (f_cost, node) = heap.pop()
      graph.current = node

      # If a node is updated with a lower cost
      # the larger cost of the node is also skipped
      if node in visited: continue

      visited.add(node)
      node.visited = True
      if node == goal:
        graph.graph_update(node, True)
        return

      for (neighbour, weight) in graph.graph.get_neighbours(node):
        if neighbour in visited or neighbour.obstacle: # skip walls
              continue
        
        neighbour.expanded = True
        new_f_cost = node.g_cost + weight + heuristic(neighbour, goal)
        # A more optimal path to this neighbor has been found
        if new_f_cost < neighbour.f_cost:
          neighbour.g_cost = node.g_cost + weight
          neighbour.h_cost = heuristic(neighbour, goal)
          neighbour.f_cost = neighbour.g_cost + neighbour.h_cost
          neighbour.parent = node
          heap.push((neighbour.f_cost, neighbour))

      graph.graph_update(node)
      time.sleep(graph.delay)

    print("No path")

# Heuristic function
def heuristic(node, goal, op = 'manhattan') -> float:
  if op == 'manhattan':
    return abs(node.x - goal.x) + abs(node.y - goal.y)
  if op == 'euclidian':
    return ceil(sqrt((node.x - goal.x)**2 + (node.y - goal.y)**2))


def astar_tree(start, goal, graph):
    start.f_cost = start.h_cost = heuristic(start, goal)
    # heap is ordered by f_cost rather than g_cost
    heap = MinHeap([(start.f_cost, start)])

    while heap.size > 0:
      (f_cost, node) = heap.pop()
      graph.current = node

      node.visited = True
      if node == goal:
        graph.graph_update(node, True)
        return

      for (neighbour, weight) in graph.graph.get_neighbours(node):
        if neighbour.obstacle: # skip walls
              continue
        
        neighbour.expanded = True
        new_f_cost = node.g_cost + weight + heuristic(neighbour, goal)
        # A more optimal path to this neighbor has been found
        if new_f_cost < neighbour.f_cost:
          neighbour.g_cost = node.g_cost + weight
          neighbour.h_cost = heuristic(neighbour, goal)
          neighbour.f_cost = neighbour.g_cost + neighbour.h_cost
          neighbour.parent = node
          heap.push((neighbour.f_cost, neighbour))

      graph.graph_update(node)
      time.sleep(graph.delay)

    print("No path")