# Генерация областей и в них уже равномерная генерация генерация случайных координат

import networkx as nx
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
import seaborn as sns
import math
from scipy import stats
from collections import Counter

# from db import DBSCAN_
from Plot_ import Plot


# сид генерации:
# 123 - два больших слиты в один.
# 1 - Мелкий в центре большого и два больших рядом. при epsя=90 очень хорошо определяет кластеры
# 6 - сразу два, а то и три мелких внутри больших
# 8 - хорошая, есть мелкий в большом остальные на расстоянии{Шикарный сид для кластеризации при eps-(50)(100) min_pts-4 и }
random.seed(8)

number_of_nodes_in_the_cluster = 30             # Число узлов в области
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
            if node <= (number_of_center_nodes * 30 // 100):
                # Условие на величину кластера. Первые 30% точек/кластеров получают разброс в 165 единиц
                # и соответсвенно размер кластера 330 единиц
                for id_node_ in range(number_of_nodes_in_the_cluster):
                    x, y, z = pos[node]
                    radius_obl = 150
                    x = x + random.uniform(-radius_obl, radius_obl)
                    y = y + random.uniform(-radius_obl, radius_obl)
                    z = z + random.uniform(-radius_obl, radius_obl)
                    node_list.append(
                        (id_node, {'pos': (x, y, z), 'claster_flag': node}))
                    id_node = id_node + 1
            else:
                for id_node_ in range(number_of_nodes_in_the_cluster):
                    x, y, z = pos[node]
                    radius_obl = 60
                    x = x + random.uniform(-radius_obl, radius_obl)
                    y = y + random.uniform(-radius_obl, radius_obl)
                    z = z + random.uniform(-radius_obl, radius_obl)
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

def node_attributes_selection(graph_, iter_):
    dict_of_node_attributes_ = {'id_node': [],'x': [], 'y': [], 'z': [], 'claster_flag': []}  # Участвует в отрисовке!!!
    def set_attr_node():
        dict_of_node_attributes_['id_node'].append(id_node)
        dict_of_node_attributes_['x'].append(graph_.nodes[id_node]['pos'][0])
        dict_of_node_attributes_['y'].append(graph_.nodes[id_node]['pos'][1])
        dict_of_node_attributes_['z'].append(graph_.nodes[id_node]['pos'][2])
        dict_of_node_attributes_['claster_flag'].append(graph_.nodes[id_node]['claster_flag'])
                
    if iter_ == 0:
        for id_node in graph_.nodes():
            set_attr_node()
    else:
        for id_node in graph_.nodes():
            if graph_.nodes[id_node]['claster_flag'] == -1:
                set_attr_node()
    return dict_of_node_attributes_

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

def learndb(nparr_atr_nodes, eps_, min_samples_, iter_):
    db = DBSCAN(eps=eps_, metric='euclidean', min_samples=min_samples_).fit(nparr_atr_nodes)

    # labels = db.labels_
    # print(labels)        # labels показывает к какому кластеру был отнесен элемент

    # unique, counts = np.unique(db.labels_, return_counts=True)
    # print(np.asarray((unique, counts)).T) # Вывод матрицы кластеров/элементов

    iter_ = iter_ + 1
    return db, iter_



# __________Создание объекта граф______________________________________
graph_ = nx.Graph()
node_generation(graph_, number_of_center_nodes, number_of_nodes_in_the_cluster)

# print('Число узлов - ', len(graph_.nodes))
# print(graph_.nodes.data())
print('Количество узлов - ',len(graph_.nodes))

# _____Создание словаря атрибутов узлов(содержит только координаты)______
iter_ = 0  # Число обучений алгоритма db
dict_of_node_attributes = node_attributes_selection(graph_,iter_)

# Вывод полученых координат
# print(dict_of_node_attributes)

# ____________Отрисока сгенеренных узлов до обучения алгоса______________
G = Plot(dict_of_node_attributes)
# G.plot_graph()

# ____________________Нахождение eps______________________________________
# нахерявсеэтоделал(?
# Словари с отсоритрованными по координатам узлами и списки id узлов для навигации по словарю
# dict_nodes_sorted_x, dict_nodes_sorted_y, dict_nodes_sorted_z, list_id_nodes_x, list_id_nodes_y, list_id_nodes_z  = sorting_nodes_by_cooridant()
# print(dict_nodes_sorted_x)

# Словарь соседей для каждого узла
dict_all_node_neighbors = {}
temporary_nodes_dict = {}
for node in graph_.nodes():
    temporary_nodes_dict[node] = graph_.nodes[node]

visibility = 200
for node_1 in graph_.nodes():
    for node_2 in temporary_nodes_dict:
        if node_1 != node_2:
            if graph_.nodes[node_1]['pos'][0] - visibility <= temporary_nodes_dict[node_2]['pos'][0] <= graph_.nodes[node_1]['pos'][0] + visibility:
                if graph_.nodes[node_1]['pos'][1] - visibility <= temporary_nodes_dict[node_2]['pos'][1] <= graph_.nodes[node_1]['pos'][1] + visibility:
                    if graph_.nodes[node_1]['pos'][2] - visibility <= temporary_nodes_dict[node_2]['pos'][2] <= graph_.nodes[node_1]['pos'][2] + visibility:
                        if node_1 not in dict_all_node_neighbors:
                            dict_all_node_neighbors[node_1] = {}
                            dict_all_node_neighbors[node_1][node_2] = temporary_nodes_dict[node_2]
                        else:
                            dict_all_node_neighbors[node_1][node_2] = temporary_nodes_dict[node_2]
# print(dict_all_node_neighbors) не выводи это!

# #__________Подсчет средних рассточний________________
R_nodes = {}
for node_osn in dict_all_node_neighbors:
    ro_rast = 0
    list_rast = []
    for node_neigh in dict_all_node_neighbors[node_osn]:
        rast = math.sqrt((graph_.nodes[node_osn]['pos'][0] - dict_all_node_neighbors[node_osn][node_neigh]['pos'][0])**2 +
                         (graph_.nodes[node_osn]['pos'][1] - dict_all_node_neighbors[node_osn][node_neigh]['pos'][1])**2 + 
                         (graph_.nodes[node_osn]['pos'][2] - dict_all_node_neighbors[node_osn][node_neigh]['pos'][2])**2)
        # print(rast)
        list_rast.append(rast)
    list_rast_sort = sorted(list_rast)
    list_5_neigh = list_rast_sort[:5]
    sum_5_neigh = sum(list_5_neigh)
    ro_rast = sum_5_neigh/5
    R_nodes[node_osn] = ro_rast


# sns.displot(R_nodes, bins=50)
# plt.title('Плотность расположения узлов в сети')
# plt.xlabel('Среднее расстояние соседства узлов')
# plt.ylabel('Количество узлов')
# plt.show()

# ____Вычисление eps по плотности узлов "гистограмма выше"_____
# Сортировка и создание списка расстояний R
list_R = []
for i in R_nodes:
    list_R.append(R_nodes[i])
list_R = sorted(list_R)

# Подсчет плотности_______
epsilon = (max(list_R) - min(list_R))/50
# print(max(list_R), min(list_R), epsilon)
density_R = {}
for delt_a in range(len(list_R)):
    sum_dens = 0
    for qwe_R in list_R:
        if list_R[delt_a] - epsilon <= qwe_R <= list_R[delt_a] + epsilon:
            sum_dens = sum_dens + 1
        elif qwe_R < list_R[delt_a] - epsilon:
            continue
        else: 
            break
    density_R[list_R[delt_a]] = sum_dens

list_density_R = []
for key in density_R:
    list_density_R.append(density_R[key])

iqq = [i for i in range(len(list_density_R))]
# plt.plot(iqq, list_density_R)
# plt.title('Плотность расположения узлов в сети')
# plt.xlabel('Среднее расстояние соседства узлов')
# plt.ylabel('Количество узлов')
# plt.show()

# ____________________Применяем DBSCAN___________________________________________________
# _________Подготовка атрибутов узлов для алгоритма___________
df = pd.DataFrame(dict_of_node_attributes)
# print(df)
nparr_atr_nodes = np.array(df)
# print(nparr_atr_nodes)


# ________обучение ____________
db_1, iter_ = learndb(nparr_atr_nodes, eps_=60, min_samples_=5, iter_=iter_)
count_of_cluster = len(set(db_1.labels_)) - 1
# print(count_of_cluster)
# print(db_1.labels_)

# # ________________Отрисовка результатов первого прохода db___________
# G_12 = Plot(dict_of_node_attributes)
# G_12.painting_of_clasters(db_1.labels_)

# _____________Добавление узлам меток кластера_______________
for id_node, label in enumerate(db_1.labels_):
    graph_.nodes[id_node]['claster_flag'] = label

# _________Подготовка атрибутов узлов для алгоритма_2___________

dict_of_node_attributes_2 = node_attributes_selection(graph_, iter_)
df_2 = pd.DataFrame(dict_of_node_attributes_2)
# print(df_2)
nparr_atr_nodes_2 = np.array(df_2)
# print(nparr_atr_nodes_2)

# ________обучение ____________
db_2, iter_ = learndb(nparr_atr_nodes_2, eps_=120, min_samples_=5, iter_=iter_)

# # _____________Отрисовка результатов второго прохода db_____
# G_22 = Plot(dict_of_node_attributes_2)
# G_22.painting_of_clasters(db_2.labels_)

# _____________Добавление узлам меток кластера_______________
for id_node, label in enumerate(db_2.labels_):
    if label != -1:
        graph_.nodes[dict_of_node_attributes_2['id_node'][id_node]]['claster_flag'] = label + count_of_cluster
    else:
        graph_.nodes[dict_of_node_attributes_2['id_node'][id_node]]['claster_flag'] = label

iter_ = 0 # Закончили обучать db, обнулим iter_, чтобы отрисовывать можео было все точки

# #____________График распределения кластеров после обучения DBSCAN__________________
dict_of_node_attributes_3 = node_attributes_selection(graph_, iter_)
df_plt = pd.DataFrame(dict_of_node_attributes_3)
unique, counts = np.unique(df_plt['claster_flag'], return_counts=True)
plt.bar(unique, counts)
plt.title('Распределение узлов по кластерам')
plt.grid()
plt.show()

# unique, counts = np.unique(df_plt['claster_flag'], return_counts=True)
# print(np.asarray((unique, counts)).T) # Вывод матрицы кластеров/элементов

# # ____________________Отрисока после DBSCAN_________________________
G_2 = Plot(dict_of_node_attributes_3)

# G.plot_graph()
# G_2.painting_of_clasters(dict_of_node_attributes['claster_flag'])