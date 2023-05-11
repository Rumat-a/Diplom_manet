import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt


class Plot:
    def __init__(self, graph, dict_of_node_attributes):
        self.__graph = graph # Мб пригодится в будущем
        self.__dict_of_node_attributes = dict_of_node_attributes

    def plot_graph(self):

        # Создаем трехмерную фигуру
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = self.__dict_of_node_attributes['x']
        y = self.__dict_of_node_attributes['y']
        z = self.__dict_of_node_attributes['z']    
        claster_flag = self.__dict_of_node_attributes['claster_flag']
        ax.scatter(x, y, z, c = claster_flag, s=30, cmap=plt.cm.Spectral)

        # Отображаем граф
        plt.show()

    def painting_of_clasters(self, dbscan_label):

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        x = self.__dict_of_node_attributes['x']
        y = self.__dict_of_node_attributes['y']
        z = self.__dict_of_node_attributes['z']
        ax.scatter(x, y, z, c=dbscan_label, s=30, cmap=plt.cm.Spectral)

        # Никуда не годная отрисовка ребер. 
        # каждое ребро отрисовывается отдельно. Это супер сильно грузит
        # for edge in self.__graph.edges():
        #     x1, y1, z1 = pos[edge[0]]
        #     x2, y2, z2 = pos[edge[1]]
        #     ax.plot([x1, x2], [y1, y2], [z1, z2], color='b')
        
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
