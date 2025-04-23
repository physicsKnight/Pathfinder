import pygame
import random
import math
import time

from threading import Thread
from Algorithms import config
from Graph import map

from memory_profiler import profile, memory_usage

fp=open('memory_profiler.log','w+')

speed = 60

grey = (100, 100, 100)  # undiscovered node or edge
white = (255, 255, 255)  # discovered edge or node outline
yellow = (200, 200, 0)  # current node fill
red = (200,0,0) # discovered node fill
green = (0, 255, 0)
black = (0, 0, 0)  # undiscovered node fill
blue = (50,80,160) # completed node fill and completed edge
purple = (128, 0, 128)

class GraphView:
    def __init__(self, graph, width, height):
        self.width = width
        self.height = height
        self.radius = 22
        self.graph = graph
        self.running = False
        self.edges = {}
        self.dragging = None
        self.current = None
        self.start = None
        self.goal = None
        self.solution = False
        self.solution_path = []
        self.running = True
        self.delay = 0.6
        self.algorithm = "astar"
        self.type = "graph"
        self.start_time = 0
        self.time = 0
        self.memory = 0
        self.cost = 0

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('AIP-project')
        self.screen = pygame.display.set_mode((width, height)) 
        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))
        self.font = pygame.font.SysFont("Georgia", 20)
        self.font2 = pygame.font.SysFont("Georgia", 14)
        self.nl = '\n'
        self.threads = []

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

    def set_start(self, pos):
        node = self.get_node(pos)
        if node: self.start = node

    def set_goal(self, pos):   
        node = self.get_node(pos)
        if node: self.goal = node

    def get_node(self, pos):
        for n in self.graph.get_nodes():
            if self.distance(n, pos) < self.radius:
                return n
        return None
    
    def delete_selected_node(self):
        if self.start is not None:
            edges = list(self.edges.keys())
            for edge in edges:
                if self.start in edge: 
                    del self.edges[edge]
                    
            self.graph.remove(self.start) 
            self.start = None

    def add_edge(self, node1, node2, dist):
        # Add to graph
        self.graph.add_edge(node1, node2, round(dist))
        
        # Store edge  
        self.edges[tuple(sorted((node1, node2)))] = True

    def update_edges(self, n1):
        for n2, _ in self.graph.get_neighbours(n1):
            cost = self.distance(n1, n2)
            self.graph.add_edge(n1, n2, round(cost))

    def generate_random_nodes(self, num_nodes):
        for _ in range(num_nodes):
            x = random.randint(self.radius, self.width - self.radius)
            y = random.randint(self.radius, self.height - self.radius)
            # 10% chance to make an obstacle node
            if random.random() < 0.2: 
                node = self.graph.add_node(x=x, y=y, obstacle=True)
            else:
                if all(self.distance(node, (x, y)) > 100 for node in self.graph.get_nodes()):
                    node = self.graph.add_node(x=x, y=y)
            
        self.connect_nearby_nodes()
            
    def connect_nearby_nodes(self):
        threshold = 200
        nodes = self.graph.get_nodes()
        for n1 in nodes:
            for n2 in nodes:
                if n1 != n2:
                    dist = self.distance(n1, n2)
                    if dist < threshold:
                        self.add_edge(n1, n2, dist)

        nodes = self.graph.get_nodes()
        for n1 in nodes:
            for n2 in nodes:
                if n1 != n2 and random.random() < 0.04:
                    self.add_edge(n1, n2, self.distance(n1, n2))

    def connect_selected_nodes(self):
        if self.start is not None and self.goal is not None:
            dist = self.distance(self.start, self.goal)
            self.add_edge(self.start, self.goal, dist)

    def distance(self, n1, n2):
        if isinstance(n2, map.Node):
            x2 = n2.x
            y2 = n2.y
        else: 
            x2 = n2[0]
            y2 = n2[1]

        dx = n1.x - x2
        dy = n1.y - y2
        return math.hypot(dx, dy)
    
    def reconstruct_path(self, node, out=False):
        path = [node]
        while node.parent is not None:
            node = node.parent
            path.insert(0, node)

        if out:
            s = ""
            for n in path:
                s += str(n) + " -> "
            print(s + " length:", len(path))

        return path
    
    def handle_click(self, event, right=False):
        if right:
            pos = pygame.mouse.get_pos()
        else:
            pos = event.pos
        node = self.get_node(pos)
        
        if node is None:
            node = self.graph.add_node(x=pos[0], y=pos[1])
            return

        if not right and event.button == 1: # Left click
            self.dragging = self.get_node(event.pos)
            if self.start is not None and self.start == node:
                    self.start = None
            else:
                self.start = node
        elif right or event.button == 3: # Right click
            if self.goal is not None and self.goal == node:
                    self.goal = None
            else:
                self.goal = node
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event)
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    self.dragging.x, self.dragging.y = round(event.pos[0]), round(event.pos[1])
            elif event.type == pygame.MOUSEBUTTONUP:  
                if event.button == 1:
                    if self.dragging:
                        self.update_edges(self.dragging)
                        self.dragging = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.solution = True
                    self.search(self.algorithm)
                elif event.key == pygame.K_BACKSPACE:
                    self.delete_selected_node()
                elif event.key == pygame.K_e:
                    self.connect_selected_nodes()
                elif event.key == pygame.K_g:
                    self.type = "graph"
                elif event.key == pygame.K_t:
                    self.type = "tree"
                elif event.key == pygame.K_n:
                    n = random.randint(20, 40)
                    self.start, self.goal, self.current = None, None, None
                    self.reset()
                    self.graph.clear()
                    self.edges.clear()
                    self.generate_random_nodes(n)
                    self.connect_nearby_nodes()
                elif event.key == pygame.K_1:
                    self.algorithm = "dfs"
                elif event.key == pygame.K_2:
                    self.algorithm = "bfs"
                elif event.key == pygame.K_3:
                    self.algorithm = "ucs"
                elif event.key == pygame.K_4:
                    self.algorithm = "astar"
                elif event.key == pygame.K_o:
                    if self.start is not None:
                        self.start.obstacle = True
                elif event.key == pygame.K_r:
                    self.handle_click(event, True)

    def draw(self):
        self.screen.fill(black)

        self.write(f"Algorithm: {self.algorithm},  Type: {self.type},  Cost: {self.cost},  Time: {self.time},  Memory: {self.memory} bytes", white, (10, 10), self.font)

        for edge in self.edges:
            node1 = edge[0]
            node2 = edge[1]
            self.draw_line(grey, node1, node2, 3)
            # Get middle point
            x_mid = (node1.x + node2.x) / 2  
            y_mid = (node1.y + node2.y) / 2
            cost = self.graph.get_edge_cost(node1, node2)
            self.write(f"{cost}", white, (x_mid, y_mid), self.font)

        if self.solution:
            for i in range(len(self.solution_path)-1):
                self.draw_line(green, self.solution_path[i], self.solution_path[i+1], 3)
            
        
        for n in self.graph.get_nodes():
            col1, col2 = white, white
            if n.expanded:
                col1, col2 = blue, blue
            if n.visited:
                col1, col2 = grey, grey
            if n.obstacle:
                col1, col2 = purple, purple
            if self.solution and n in self.solution_path:
                col1, col2 = green, green
            if self.current is not None and n == self.current:
                col1, col2 = yellow, yellow
            if n == self.start:
                col1, col2, = white, green
            elif n == self.goal:
                col1, col2 = white, red

            self.circle_fill((n.x, n.y), col1, col2, self.radius, 2)

            offset = (int(self.radius / 2), int(self.radius / 2))
            centered_pos_x = (n.x - offset[0]-3, n.y - offset[1]-6)
            centered_pos_y = (n.x - offset[0]-3, n.y - offset[1]+6)

            if not n.obstacle:
                self.write(f"{n.x},", black, centered_pos_x, self.font2)
                self.write(f"{n.y}", black, centered_pos_y, self.font2)
        self.update()

    def search(self, algorithm):
        if self.start is None or self.goal is None:
            print("Start or goal node not found in the graph.")
            return

        if algorithm in config.algorithms:
            self.reset()
            i = 0 if self.type == "graph" else 1
            algorithm = config.algorithms[algorithm][i]
            self.threadExecutor(algorithm, self.start, self.goal, self)
        else:
            print("Invalid algorithm specified.")

    @profile(stream=fp)
    def execute_function(self, function, *args):
        try:
            function(*args)
        except Exception as e:
            print(f"Exception in background thread: {e}")

    def threadExecutor(self, function, *args):
        if self.threads:
            for thread in self.threads:
                thread.join()
            self.threads.clear()

        self.threads.append(Thread(target=self.execute_function, args=(function, *args)))
        self.threads[0].daemon = True # stops execution of thread when it is removed
        self.threads[0].start()

    def graph_update(self, node, out=False):
        node.discovery = time.process_time()
        self.time = node.discovery - self.start_time
        self.current = node
        self.solution_path = self.reconstruct_path(node, out)
        self.cost = node.cost if self.algorithm == 'ucs' else node.g_cost
        self.memory = round(memory_usage()[0], 4)

    def update(self):
        pygame.display.update()
        self.clock.tick(speed)

    def reset(self):
        self.start_time = time.process_time()
        self.time = 0
        self.memory = 0
        self.cost = 0
        self.solution_path.clear()
        self.graph.reset()

    def circle_fill(self, xy, line_colour, fill_colour, radius, thickness):
        pygame.draw.circle(self.screen, line_colour, xy, radius)
        pygame.draw.circle(self.screen, fill_colour, xy, radius - thickness)

    def draw_line(self, line_colour, n1, n2, width=2):
        pygame.draw.line(self.screen, line_colour, (n1.x, n1.y), (n2.x, n2.y), width)
    
    def write(self, text, colour, pos, font):
        self.screen.blit(font.render(text, True, colour), pos)