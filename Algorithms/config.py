from Algorithms.Astar import Astar
from Algorithms.UCS import UCS
from Algorithms.BFS import bfs
from Algorithms.DFS import dfs
from Graph import map, maze

algorithms = {
    'astar': [Astar.astar, Astar.astar_tree],
    'ucs': [UCS.uniform_cost_search, UCS.uniform_cost_search_tree],
    'bfs': [bfs.bfs, bfs.bfs_tree],
    'dfs': [dfs.dfs, dfs.dfs_tree]
}

def create_maze(start_x, start_y):
    start_node = map.get_node(map.graph, start_x, start_y)
    maze.generate_maze(map.graph, start_node)
    goal_x, goal_y = maze.generate_goal(map.graph)
    return goal_x, goal_y