import random
from Graph import map

# Generate a maze using DFS by using recursion
def generate_maze(graph, current_node, probability=0.8):
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        next_x, next_y = current_node.x + dx, current_node.y + dy

        if 0 <= next_x < map.GRID_SIZE and 0 <= next_y < map.GRID_SIZE:
            neighbor = map.get_node(graph, next_x, next_y)
            if neighbor.wall and random.random() < probability:
                # Mark the neighbor as not a wall
                neighbor.wall = False
                # Remove the wall between the current cell and the neighbor
                graph[(current_node.x + next_x) // 2][(current_node.y + next_y) // 2].wall = False
                # Recursively generate the maze from the neighbor
                generate_maze(graph, neighbor, probability)


def generate_goal(graph):
    open_nodes = []
    for row in graph:
        for node in row:
            if not node.wall:
                open_nodes.append((node.x, node.y))
    
    goal_x, goal_y = random.choice(open_nodes)
    return goal_x, goal_y
