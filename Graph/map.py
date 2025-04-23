class Graph:
    def __init__(self, nodes=0):
        # each node has a dictionary of neighbours
        self.nodes = nodes
        self.adjList = {}

    def add_node(self, x, y, obstacle=False):
        self.nodes += 1
        node = Node(x=x, y=y, obstacle=obstacle)
        node.id = self.nodes
        self.adjList[node] = {}
        return node
    
    def add_edge(self, s, d, cost=0, directed=False):
        self.adjList[s][d] = cost
        if not directed:
            self.adjList[d][s] = cost
    
    def get_neighbours(self, node):
        return self.adjList[node].items()  
    
    def get_edge_cost(self, node1, node2):
        if node1 in self.adjList and node2 in self.adjList[node1]:
            return self.adjList[node1][node2]
        elif node2 in self.adjList and node1 in self.adjList[node2]:
            return self.adjList[node2][node1]
        else:
            return None
            
    def get_nodes(self):
        return self.adjList.keys()
    
    def remove(self, node):
        del self.adjList[node]
        self.nodes -= 1

    def reset(self):
        for node in self.get_nodes():
            node.reset()

    def clear(self):
        self.adjList.clear()
        self.nodes = 0

    def __str__(self):
        result = ""
        for node, neighbors in self.adjList.items():
            result += f"Node {node.id}, {node.x}, {node.y} - Neighbors: "
            for neighbor, cost in neighbors.items():
                result += f"({neighbor.id}, cost={cost}), "
            result = result.rstrip(", ") + "\n"
        return result
        
    def __contains__(self, n):
        return n in self.adjList

class Node:
    def __init__(self, x=0, y=0, c=0, parent=None, obstacle=False):
        self.id = None
        self.x = x # x coordinate
        self.y = y # y corrdinate
        self.cost = float('inf') # g_cost
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = float('inf')
        self.parent = parent # node of parent
        self.obstacle = obstacle # blocked node
        self.visited = False
        self.expanded = False
        self.discovery = 0

    def reset(self):
        self.cost = float('inf') # g_cost
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = float('inf')
        self.parent = None # node of parent
        self.visited = False
        self.expanded = False
        self.discovery = 0

    def __str__(self):
        return f"Node({self.x}, {self.y})"
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __hash__(self):
        return hash((self.id))
