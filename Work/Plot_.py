import networkx as nx
import random
import matplotlib.pyplot as plt


class Plot:
    def __init__(self, graph):
        self.__graph = graph

    def plot_graph(self):
        pos = nx.get_node_attributes(self.__graph, 'pos')
        colorr = nx.get_node_attributes(self.__graph, 'color')

        # Создаем трехмерную фигуру
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Рисуем вершины и ребра
        for node in self.__graph.nodes():
            x, y, z = pos[node]
            cl = colorr[node]
            # cl = (0, 0, 0)
            ax.scatter(x, y, z, color=cl)
        for edge in self.__graph.edges():
            x1, y1, z1 = pos[edge[0]]
            x2, y2, z2 = pos[edge[1]]
            ax.plot([x1, x2], [y1, y2], [z1, z2], color='b')

        # Отображаем граф
        plt.show()


# # Проверка__________________________________________________________
# h = nx.Graph()
# h.add_edges_from([(1, 2), (3, 1), (2, 4), (2, 5), (5, 6), (6, 1), (2, 3)])
# h.add_node(1, pos=(1, 1, 3), color=(round(random.random(), 2), round(random.random(), 2), round(random.random(), 2)))
# h.add_node(2, pos=(1, 2, 1), color=(round(random.random(), 2), round(random.random(), 2), round(random.random(), 2)))
# h.add_node(3, pos=(2, 4, 2), color=(round(random.random(), 2), round(random.random(), 2), round(random.random(), 2)))
# h.add_node(4, pos=(2, 4, 1), color=(round(random.random(), 2), round(random.random(), 2), round(random.random(), 2)))
# h.add_node(5, pos=(1, 3, 4), color=(round(random.random(), 2), round(random.random(), 2), round(random.random(), 2)))
# h.add_node(6, pos=(2, 1, 1), color=(round(random.random(), 2), round(random.random(), 2), round(random.random(), 2)))

# G = Plot(h)
# G.plot_graph()
