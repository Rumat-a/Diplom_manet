# Генерация областей и в них уже равномерная генерация генерация случайных координат

import networkx as nx
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from Plot_ import Plot
from sklearn.cluster import DBSCAN

# сид генерации 123 
random.seed(123)


def node_generation(graph_, number_of_center_nodes, number_of_nodes_in_the_cluster):
    # Генерация точек центров.
    def generating_center_nodes(graph_, number_of_center_nodes):
        for id_node in range(number_of_center_nodes):
            x = random.uniform(0, 1000)
            y = random.uniform(0, 1000)
            z = random.uniform(0, 1000)
            graph_.add_node(id_node, pos=(x, y, z), color=(1, 0, 0))

    def generating_the_remaining_nodes(graph_, number_of_center_nodes):
        pos = nx.get_node_attributes(graph_, 'pos')
        node_list = []
        # id_node - номер узла в графе, задаем с учетом "len(graph_) - 1" тех номеров, что уже есть в графе 
        id_node = len(graph_)
        # Перебор центровых/графовых точек 
        for node in graph_.nodes():
            # Генерация узлов вокруг центральной точки
            if node <= (number_of_center_nodes * 40 // 100):
                # Условие на величину кластера. Первые 30% точек/кластеров получают разброс в 165 единиц 
                # и соответсвенно размер кластера 330 единиц
                col_ = (round(random.uniform(0, 0.5), 2),round(random.random(), 2), round(random.uniform(0, 0.5), 2))
                for id_node_ in range(number_of_nodes_in_the_cluster):
                    x, y, z = pos[node]
                    x = x + random.uniform(-190, 190)
                    y = y + random.uniform(-190, 190)
                    z = z + random.uniform(-190, 190)
                    node_list.append((id_node, {'pos': (x, y, z), 'color': col_}))
                    id_node = id_node + 1
            else:
                col_ = (round(random.uniform(0, 0.5), 2),round(random.uniform(0, 0.5), 2), round(random.random(), 2))
                for id_node_ in range(number_of_nodes_in_the_cluster):
                    x, y, z = pos[node]
                    x = x + random.uniform(-82, 82)
                    y = y + random.uniform(-82, 82)
                    z = z + random.uniform(-82, 82)
                    node_list.append((id_node, {'pos': (x, y, z), 'color': col_}))
                    id_node = id_node + 1
        graph_.add_nodes_from(node_list)
    
    def generating_noise_nodes(graph_):
        noice_nodes_list = []
        id_node = len(graph_)
        for i in range(len(graph_) * 30 // 100):
            x = random.uniform(0, 1000)
            y = random.uniform(0, 1000)
            z = random.uniform(0, 1000)
            noice_nodes_list.append((id_node, {'pos': (x, y, z), 'color': (0, 0, 0)}))
            id_node = id_node + 1
        graph_.add_nodes_from(noice_nodes_list)

    generating_center_nodes(graph_, number_of_center_nodes)
    generating_the_remaining_nodes(graph_, number_of_center_nodes)
    generating_noise_nodes(graph_)


graph = nx.Graph()
node_generation(graph_=graph, number_of_center_nodes=10, number_of_nodes_in_the_cluster=20)

# print('Число узлов - ', len(graph.nodes))
# print(graph.nodes.data())
# print(graph.nodes[123])

# Создание словаря атрибутов узлов(содержит только координаты)
dict_of_node_attributes = {'x': [], 'y':[], 'z':[]}
for id_ndoe in graph.nodes():
    dict_of_node_attributes['x'].append(graph.nodes[id_ndoe]['pos'][0])
    dict_of_node_attributes['y'].append(graph.nodes[id_ndoe]['pos'][1])
    dict_of_node_attributes['z'].append(graph.nodes[id_ndoe]['pos'][2])




# # вывод элементов словарь атрибутов узлов
for key in dict_of_node_attributes:
    # print(key)
    print(dict_of_node_attributes[key])

# ____________________Применяем DBSCAN___________________
df = pd.DataFrame(dict_of_node_attributes)
# Получилось 272 строки, каждая из которых это узел 
print(df)


X = np.array(df)
db = DBSCAN().fit(X)
labels = db.labels_
# labels показывает к какому кластеру был отнесен элемент
print(labels)


# ____________________Отрисока____________________________
# G = Plot(graph)
# G.plot_graph()


