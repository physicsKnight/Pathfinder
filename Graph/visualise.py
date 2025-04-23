import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(10, 10))

def Visualise(graph, start, goal, path=None):
    ax.clear()

    # Draw the grid with a white background
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            node = graph[i][j]
            if node == start:
                color = 'green'  # Color for start node
            elif node == goal:
                color = 'red'   # Color for goal node
            else:
                color = 'brown' if node.wall else 'gray' if path is None or not path or node not in path else 'orange'

            rect = Rectangle((j, i), 1, 1, facecolor=color, edgecolor='black')
            ax.add_patch(rect)

            # Add cost information
            text_x = j + 0.5
            text_y = i + 0.5
            plt.text(text_x, text_y, f'{node.cost}, {node.h_cost}\n{node.f_cost}',
                     fontsize=8, color='black', ha='center', va='center')

    plt.xlim(0, len(graph[0]))
    plt.ylim(0, len(graph))
    plt.gca().set_aspect('equal', adjustable='box')

    plt.draw()
    plt.pause(0.1)  # Introduce a delay (adjust the value as needed)

def reconstruct_path(node):
  path = [node]
  while node.parent is not None:
    node = node.parent
    path.insert(0, node)
  return path

def update(node, graph, start, goal):
    path = reconstruct_path(node)
    Visualise(graph, start, goal, path)





