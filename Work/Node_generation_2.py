# Генерация областей и в них уже равномерная генерация генерация случайных координат

import networkx as nx
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

from Plot_ import Plot

# сид генерации: 
# 123 - два больших слиты в один.
# 1 - Мелкий в центре большого и два больших рядом. при epsя=90 очень хорошо определяет кластеры
# 6 - сразу два, а то и три мелких внутри больших 
random.seed(6)

number_of_nodes_in_the_cluster = 40             # Число узлов в области 
number_of_center_nodes = 10                     # Число центров областей генерации точек 

def node_generation(graph_, number_of_center_nodes, number_of_nodes_in_the_cluster):
    # Генерация точек центров.
    def generating_center_nodes(graph_, number_of_center_nodes):
        for id_node in range(number_of_center_nodes):
            x = random.uniform(0, 1000)
            y = random.uniform(0, 1000)
            z = random.uniform(0, 1000)
            graph_.add_node(id_node, pos=(x, y, z), claster_flag=-2)

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
                for id_node_ in range(number_of_nodes_in_the_cluster):
                    x, y, z = pos[node]
                    x = x + random.uniform(-150, 150)
                    y = y + random.uniform(-150, 150)
                    z = z + random.uniform(-150, 150)
                    node_list.append(
                        (id_node, {'pos': (x, y, z), 'claster_flag': node}))
                    id_node = id_node + 1
            else:
                for id_node_ in range(number_of_nodes_in_the_cluster):
                    x, y, z = pos[node]
                    x = x + random.uniform(-60, 60)
                    y = y + random.uniform(-60, 60)
                    z = z + random.uniform(-60, 60)
                    node_list.append(
                        (id_node, {'pos': (x, y, z), 'claster_flag': node}))
                    id_node = id_node + 1
        graph_.add_nodes_from(node_list)

    def generating_noise_nodes(graph_):
        noice_nodes_list = []
        id_node = len(graph_)
        # Шумовых точек 20% от числа всех точек в графе на данный момент
        for i in range(len(graph_) * 20 // 100):
            x = random.uniform(0, 1000)
            y = random.uniform(0, 1000)
            z = random.uniform(0, 1000)
            noice_nodes_list.append(
                (id_node, {'pos': (x, y, z), 'claster_flag': -1}))
            id_node = id_node + 1
        graph_.add_nodes_from(noice_nodes_list)

    generating_center_nodes(graph_, number_of_center_nodes)
    generating_the_remaining_nodes(graph_, number_of_center_nodes)
    generating_noise_nodes(graph_)

def node_attributes_selection(graph_):
    dict_of_node_attributes = {'x': [], 'y': [], 'z': [], 'claster_flag': []} # Участвует в отрисовке!!!
    for id_ndoe in graph_.nodes():
        dict_of_node_attributes['x'].append(graph.nodes[id_ndoe]['pos'][0])
        dict_of_node_attributes['y'].append(graph.nodes[id_ndoe]['pos'][1])
        dict_of_node_attributes['z'].append(graph.nodes[id_ndoe]['pos'][2])
        dict_of_node_attributes['claster_flag'].append(graph.nodes[id_ndoe]['claster_flag'])
    return dict_of_node_attributes

# Функция сортироваки узлов по координате
def sorting_nodes_by_cooridant():
    coord_list = ['x', 'y', 'z']
    nodes_sorted_x = {}
    nodes_sorted_y = {}
    nodes_sorted_z = {}
    list_id_nodes_x = []
    list_id_nodes_y = []
    list_id_nodes_z = []
    for coord in coord_list:
        # словарь для id узлов и текущей координаты
        idnodes_coord = {}
        for index, value in enumerate(dict_of_node_attributes[coord]):
            idnodes_coord[index] = value
        # print(idnodes_coord)

        # Словарь отсортированных узлов
        nodes_sorted_coord = {}
        # список id узлов для навигации по словарю
        list_id_nodes_coord = []
        # Отсортированные ключи словаря
        sorted_id_ndoes = sorted(idnodes_coord, key=idnodes_coord.get)
        for key in sorted_id_ndoes:
            nodes_sorted_coord[key] = idnodes_coord[key]
            list_id_nodes_coord.append(key)
        
        if coord == 'x':
             nodes_sorted_x = nodes_sorted_coord
        elif coord == 'y':
             nodes_sorted_y = nodes_sorted_coord
        elif coord == 'z':
             nodes_sorted_z = nodes_sorted_coord

        # Вывод
        # ig = 0
        # for key in nodes_sorted_coord:
        #     print(list_id_nodes_coord[ig])
        #     print(key, nodes_sorted_coord[key])
        #     ig = ig + 1
    return nodes_sorted_x, nodes_sorted_y, nodes_sorted_z, list_id_nodes_x, list_id_nodes_y, list_id_nodes_z
    

graph = nx.Graph()
node_generation(graph, number_of_center_nodes, number_of_nodes_in_the_cluster)

# print('Число узлов - ', len(graph.nodes))
# print(graph.nodes.data())
# print(graph.nodes[123])

# Создание словаря атрибутов узлов(содержит только координаты)
dict_of_node_attributes = node_attributes_selection(graph)


# ____________________Вывод полученых координат______________________
# print(dict_of_node_attributes)

# __________________Отрисока сгенеренных узлов до обучения алгоса____
G = Plot(graph, dict_of_node_attributes)
G.plot_graph()


# ___________________Подготовка атрибутов узлов для алгоритма________
df = pd.DataFrame(dict_of_node_attributes)
# Получилось 272 строки, каждая из которых это узел
# print(df)
X = np.array(df)
# print(X)

# ____________________Нахождение eps_________________________________
# нахерявсеэтоделал(?
# Словари с отсоритрованными по координатам узлами и списки id узлов для навигации по словарю 
# dict_nodes_sorted_x, dict_nodes_sorted_y, dict_nodes_sorted_z, list_id_nodes_x, list_id_nodes_y, list_id_nodes_z  = sorting_nodes_by_cooridant()
# print(dict_nodes_sorted_x)

# Словарь соседей для каждого узла
dict_all_node_neighbors = {}
temporary_nodes_dict = {}
for node in graph.nodes():
    temporary_nodes_dict[node] = graph.nodes[node]

visibility = 100
for node_1 in graph.nodes():
    for node_2 in temporary_nodes_dict:
        if node_1 != node_2:
            if graph.nodes[node_1]['pos'][0] - visibility <= temporary_nodes_dict[node_2]['pos'][0] <= graph.nodes[node_1]['pos'][0] + visibility:
                if graph.nodes[node_1]['pos'][1] - visibility <= temporary_nodes_dict[node_2]['pos'][1] <= graph.nodes[node_1]['pos'][1] + visibility:
                    if graph.nodes[node_1]['pos'][2] - visibility <= temporary_nodes_dict[node_2]['pos'][2] <= graph.nodes[node_1]['pos'][2] + visibility:
                        if node_1 not in dict_all_node_neighbors:
                            dict_all_node_neighbors[node_1] = {}
                            dict_all_node_neighbors[node_1][node_2] = temporary_nodes_dict[node_2]
                        else:
                            dict_all_node_neighbors[node_1][node_2] = temporary_nodes_dict[node_2]


# print(dict_all_node_neighbors) не выводи это!


# ____________________Применяем DBSCAN(есть в отдельном классе)______

db = DBSCAN(eps=80, metric='euclidean', min_samples=4).fit(X)
labels = db.labels_
# labels показывает к какому кластеру был отнесен элемент
# print(labels)

unique, counts = np.unique(db.labels_, return_counts=True)
# print(np.asarray((unique, counts)).T)


# # ____________________Добавление узлам меток кластера_______________
# это показывает как правильно добавить метки кластеров узлам
# for i in range(5):
#     print('graph[i]: ', graph.nodes[i], 
#          ' | db.labels_[i]: ', db.labels_[i],
#          ' | df.iloc[i]: ', round(df.iloc[i]['x'], 2), round(df.iloc[i]['y'], 2), round(df.iloc[i]['z'], 2))
# # graph[i]:  {'pos': (52.36359, 87.186, 407.2417), 'claster_flag': (1, 0, 0)}  | db.labels_[i]:  6  | df.iloc[i]:  52.36 87.19 407.24

for id_node, label in enumerate(db.labels_):
    graph.nodes[id_node]['claster_flag'] = label

# # ____________________Отрисока после DBSCAN_________________________
G_2 = Plot(graph, dict_of_node_attributes)
G_2.painting_of_clasters(db.labels_)

