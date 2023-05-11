# Генерация узлов в одной области
import networkx as nx
import random
import matplotlib.pyplot as plt


def node_generation(graph_, number_of_nodes):
    for id_node in range(number_of_nodes):
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        z = random.uniform(0, 1000)
        graph_.add_node(id_node, pos=(x, y, z))


graph = nx.Graph()

node_generation(graph, 40)

pos = nx.get_node_attributes(graph, 'pos')
# print(pos)

# Создаем трехмерную фигуру
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Рисуем вершины и ребра
for node in graph.nodes():
    x, y, z = pos[node]
    ax.scatter(x, y, z, color='b')
for edge in graph.edges():
    x1, y1, z1 = pos[edge[0]]
    x2, y2, z2 = pos[edge[1]]
    ax.plot([x1, x2], [y1, y2], [z1, z2], color='b')

# Отображаем граф
plt.show()
