from Graph import map
from draw import GraphView

width = 1280
height = 720

if __name__ == '__main__':
    graph = map.Graph()
    graphview = GraphView(graph, width, height)
    graphview.generate_random_nodes(40)
    graphview.connect_nearby_nodes()
    graphview.run()
