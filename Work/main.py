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

# Число узлов в области
number_of_nodes_in_the_cluster = 30             
# Число центров областей генерации точек
number_of_center_nodes = 10
# Область видимости узла 
visibility = 200
# Пропускная способность ребра (канала связи между узлами) bandwigth (mb/c)
bw = 100



def node_generation(graph_, number_of_center_nodes, number_of_nodes_in_the_cluster, default_center_graphs_):
    'Генерация узлов'
    # Генерация точек центров.
    def generating_center_nodes(graph_, number_of_center_nodes):
        node_list = []
        default_center_graphs_list = []
        for id_node in range(number_of_center_nodes):
            x = random.uniform(0, 1000)
            y = random.uniform(0, 1000)
            z = random.uniform(0, 1000)
            node_list.append((id_node, {'x': x, 'y': y, 'z': z, 'claster_flag': -2, 'role': 'root', 'default_space': id_node}))
            default_center_graphs_[id_node] = {'x': x, 'y': y, 'z': z, 'claster_flag': -2, 'role': 'root', 'default_space': id_node}
        graph_.add_nodes_from(node_list)



    def generating_the_remaining_nodes(graph_, number_of_center_nodes):
        # pos = nx.get_node_attributes(graph_, 'pos')
        node_list = []
        # id_node - номер узла в графе, задаем с учетом "len(graph_) - 1" тех номеров, что уже есть в графе
        id_node = len(graph_)
        # Перебор корневых/графовых точек
        for node in graph_.nodes():
            # Генерация узлов вокруг центральной точки
            if node <= (number_of_center_nodes * 30 // 100):
                # Условие на величину кластера. Первые 30% точек/кластеров получают разброс в 165 единиц
                # и соответсвенно размер кластера 330 единиц
                for i in range(number_of_nodes_in_the_cluster):
                    x = graph_.nodes[node]['x']
                    y = graph_.nodes[node]['y']
                    z = graph_.nodes[node]['z']
                    radius_obl = 150
                    x = x + random.uniform(-radius_obl, radius_obl)
                    y = y + random.uniform(-radius_obl, radius_obl)
                    z = z + random.uniform(-radius_obl, radius_obl)
                    node_list.append((id_node, {'x': x, 'y': y, 'z': z, 'claster_flag': node, 'role': 'node', 'default_space': node, 'radius_obl': radius_obl}))
                    id_node = id_node + 1
            else:
                for i in range(number_of_nodes_in_the_cluster):
                    x = graph_.nodes[node]['x']
                    y = graph_.nodes[node]['y']
                    z = graph_.nodes[node]['z']
                    radius_obl = 60
                    x = x + random.uniform(-radius_obl, radius_obl)
                    y = y + random.uniform(-radius_obl, radius_obl)
                    z = z + random.uniform(-radius_obl, radius_obl)
                    node_list.append((id_node, {'x': x, 'y': y, 'z': z, 'claster_flag': node, 'role': 'node', 'default_space': node, 'radius_obl': radius_obl}))
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
            noice_nodes_list.append((id_node, {'x': x, 'y': y, 'z': z, 'claster_flag': -1, 'role': 'noiz', 'default_space': -1}))
            id_node = id_node + 1
        graph_.add_nodes_from(noice_nodes_list)

    generating_center_nodes(graph_, number_of_center_nodes)
    generating_the_remaining_nodes(graph_, number_of_center_nodes)
    generating_noise_nodes(graph_)


def node_attributes_selection(graph_, iter_):
    'Создание списка атрибутов узла'

    dict_of_node_attributes_ = {'id_node': [], 'x': [], 'y': [], 'z': [], 'claster_flag': []}  # Участвует в отрисовке!!!

    def set_attr_node():
        dict_of_node_attributes_['id_node'].append(id_node)
        dict_of_node_attributes_['x'].append(graph_.nodes[id_node]['x'])
        dict_of_node_attributes_['y'].append(graph_.nodes[id_node]['y'])
        dict_of_node_attributes_['z'].append(graph_.nodes[id_node]['z'])
        dict_of_node_attributes_['claster_flag'].append(
            graph_.nodes[id_node]['claster_flag'])

    if iter_ == 0:
        for id_node in graph_.nodes():
            set_attr_node()
    else:
        for id_node in graph_.nodes():
            if graph_.nodes[id_node]['claster_flag'] == -1:
                set_attr_node()
    return dict_of_node_attributes_


def learndb(nparr_atr_nodes, eps_, min_samples_, iter_):
    'Обучение db'

    db = DBSCAN(eps=eps_, metric='euclidean',
                min_samples=min_samples_).fit(nparr_atr_nodes)

    # labels = db.labels_
    # print(labels)        # labels показывает к какому кластеру был отнесен элемент

    # unique, counts = np.unique(db.labels_, return_counts=True)
    # print(np.asarray((unique, counts)).T) # Вывод матрицы кластеров/элементов

    iter_ = iter_ + 1
    return db, iter_
  

def shift_coord(graph_, default_center_graphs_):
    'Движение узлов'

    for node in graph_.nodes():
        shift = 80
        if graph.nodes[node]['role'] == 'noiz':

            X_def = graph_.nodes[node]['x']
            graph_.nodes[node]['x'] = graph_.nodes[node]['x'] + random.uniform(-shift, shift)
            if 0 > graph_.nodes[node]['x'] or graph_.nodes[node]['x'] > 1000:
                while 0 > graph_.nodes[node]['x'] or graph_.nodes[node]['x'] > 1000:
                    graph_.nodes[node]['x'] = X_def
                    graph_.nodes[node]['x'] = graph_.nodes[node]['x'] + random.uniform(-shift, shift)
            
            Y_def = graph_.nodes[node]['y']
            graph_.nodes[node]['y'] = graph_.nodes[node]['y'] + random.uniform(-shift, shift)
            if 0 > graph_.nodes[node]['y'] or graph_.nodes[node]['y'] > 1000:
                while 0 > graph_.nodes[node]['y'] or graph_.nodes[node]['y'] > 1000:
                    graph_.nodes[node]['y'] = Y_def
                    graph_.nodes[node]['y'] = graph_.nodes[node]['y'] + random.uniform(-shift, shift)

            Z_def = graph_.nodes[node]['z']
            graph_.nodes[node]['z'] = graph_.nodes[node]['z'] + random.uniform(-shift, shift)
            if 0 > graph_.nodes[node]['z'] or graph_.nodes[node]['z'] > 1000:
                while 0 > graph_.nodes[node]['z'] or graph_.nodes[node]['z'] > 1000:
                    graph_.nodes[node]['z'] = Z_def
                    graph_.nodes[node]['z'] = graph_.nodes[node]['z'] + random.uniform(-shift, shift)
        
        else:
            default_space = graph.nodes[node]['default_space']
            if graph.nodes[node]['role'] == 'node':
                
                # Генерация координат в области кластера
                X_def = graph_.nodes[node]['x']
                graph_.nodes[node]['x'] = graph_.nodes[node]['x'] + random.uniform(-shift, shift)
                a = default_center_graphs_[default_space]['x']
                b = graph_.nodes[node]['radius_obl']
                c = graph_.nodes[node]['x']
                if a - b > c or c > a + b:
                    while default_center_graphs_[default_space]['x'] - graph_.nodes[node]['radius_obl'] > graph_.nodes[node]['x'] or graph_.nodes[node]['x'] > default_center_graphs_[default_space]['x'] + graph_.nodes[node]['radius_obl']:
                        graph_.nodes[node]['x'] = X_def
                        graph_.nodes[node]['x'] = graph_.nodes[node]['x'] + random.uniform(-shift, shift)

                Y_def = graph_.nodes[node]['y']
                graph_.nodes[node]['y'] = graph_.nodes[node]['y'] + random.uniform(-shift, shift)
                if default_center_graphs_[default_space]['y'] - graph_.nodes[node]['radius_obl'] > graph_.nodes[node]['y'] or graph_.nodes[node]['y'] > default_center_graphs_[default_space]['y'] + graph_.nodes[node]['radius_obl']:
                    while default_center_graphs_[default_space]['y'] - graph_.nodes[node]['radius_obl'] > graph_.nodes[node]['y'] or graph_.nodes[node]['y'] > default_center_graphs_[default_space]['y'] + graph_.nodes[node]['radius_obl']:
                        graph_.nodes[node]['y'] = Y_def
                        graph_.nodes[node]['y'] = graph_.nodes[node]['y'] + random.uniform(-shift, shift)
                
                Z_def = graph_.nodes[node]['z']
                graph_.nodes[node]['z'] = graph_.nodes[node]['z'] + random.uniform(-shift, shift)
                if default_center_graphs_[default_space]['z'] - graph_.nodes[node]['radius_obl'] > graph_.nodes[node]['z'] or graph_.nodes[node]['z'] > default_center_graphs_[default_space]['z'] + graph_.nodes[node]['radius_obl']:
                    while default_center_graphs_[default_space]['z'] - graph_.nodes[node]['radius_obl'] > graph_.nodes[node]['z'] or graph_.nodes[node]['z'] > default_center_graphs_[default_space]['z'] + graph_.nodes[node]['radius_obl']:
                        graph_.nodes[node]['z'] = Z_def
                        graph_.nodes[node]['z'] = graph_.nodes[node]['z'] + random.uniform(-shift, shift)                


def finding_neighbors_of_nodes(graph_, visibility):
    'Нахождение соседей для каждого узла'

    dict_all_node_neighbors = {}
    temporary_nodes_dict = {}
    for node in graph_.nodes():
        temporary_nodes_dict[node] = graph_.nodes[node]

    # vis - Область видимости в пределах которой находятся соседи
    vis = visibility
    for node_1 in graph_.nodes():
        for node_2 in temporary_nodes_dict:
            if node_1 != node_2:
                if graph_.nodes[node_1]['x'] - vis < temporary_nodes_dict[node_2]['x'] < graph_.nodes[node_1]['x'] + vis:
                    if graph_.nodes[node_1]['y'] - vis < temporary_nodes_dict[node_2]['y'] < graph_.nodes[node_1]['y'] + vis:
                        if graph_.nodes[node_1]['z'] - vis < temporary_nodes_dict[node_2]['z'] < graph_.nodes[node_1]['z'] + vis:
                            if node_1 not in dict_all_node_neighbors:
                                dict_all_node_neighbors[node_1] = {}
                                dict_all_node_neighbors[node_1][node_2] = temporary_nodes_dict[node_2]
                            else:
                                dict_all_node_neighbors[node_1][node_2] = temporary_nodes_dict[node_2]
    # print(dict_all_node_neighbors) не выводи это!

    return dict_all_node_neighbors


def edge_generation(graph, dict_all_node_neighbors_, bw_, visibility_):
    'Добавление ребер между узлами'

    for target_node in dict_all_node_neighbors_:
        for neighbor_node in dict_all_node_neighbors_[target_node]:
            # Если узлы принадлежат одному кластеру
            if graph.nodes[target_node]['claster_flag'] == graph.nodes[neighbor_node]['claster_flag']:
                # Если такого ребра еще нет в графе 
                if graph.has_edge(target_node, neighbor_node) == False and graph.has_edge(neighbor_node, target_node) == False:
                    # расстояние между узлами
                    rast = math.sqrt((graph.nodes[target_node]['x'] - dict_all_node_neighbors_[target_node][neighbor_node]['x'])**2 + 
                                    (graph.nodes[target_node]['y'] - dict_all_node_neighbors_[target_node][neighbor_node]['y'])**2 +
                                    (graph.nodes[target_node]['z'] - dict_all_node_neighbors_[target_node][neighbor_node]['z'])**2)
                    # пропускная способность канала между узлами с учетом расстояния между ними
                    # ГДЕ УТЕЧКА!? rast НЕ ДОЛЖЕН ПРИВЫШАТЬ 100!
                    bw_rast = bw_ * (rast/(visibility_ * math.sqrt(2) * 1.1))

                    graph.add_edge(target_node, neighbor_node, weight=bw_rast)
    
    # Проверка на утечку
    # for n, nbrs in graph.adj.items():
    #     for nbr, eattr_ in nbrs.items():
    #         if eattr_['weight'] >= 100:
    #             print(n, nbr, eattr_['weight'])


def сalculating_average_distances(graph_, dict_all_node_neighbors_, steps_):
    'Рассчет расстояния соседства'

    R_nodes_ = {}
    for node_osn in dict_all_node_neighbors_:
        ro_rast = 0
        list_rast = []
        for node_neigh in dict_all_node_neighbors_[node_osn]:
            rast = math.sqrt((graph_.nodes[node_osn]['x'] - dict_all_node_neighbors_[node_osn][node_neigh]['x'])**2 +
                             (graph_.nodes[node_osn]['y'] - dict_all_node_neighbors_[node_osn][node_neigh]['y'])**2 +
                             (graph_.nodes[node_osn]['z'] - dict_all_node_neighbors_[node_osn][node_neigh]['z'])**2)
            # print(rast)
            list_rast.append(rast)
        list_rast_sort = sorted(list_rast)
        list_5_neigh = list_rast_sort[:5]
        sum_5_neigh = sum(list_5_neigh)
        ro_rast = sum_5_neigh/5
        R_nodes_[node_osn] = ro_rast

    # if steps == 1:
    #     sns.displot(R_nodes_, bins=50)
    #     plt.title('Плотность расположения узлов в сети')
    #     plt.xlabel('Среднее расстояние соседства узлов')
    #     plt.ylabel('Количество узлов')
    #     plt.show()
    # sns.displot(R_nodes_, bins=50)
    # plt.title('Плотность расположения узлов в сети')
    # plt.xlabel('Среднее расстояние соседства узлов')
    # plt.ylabel('Количество узлов')
    # plt.show()


    return R_nodes_


def sorting_and_creating_a_list_of_distances_R(R_nodes_):
    'Сортировка и создание списка расстояний R'

    list_R = []
    for i in R_nodes_:
        list_R.append(R_nodes_[i])
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


def finding_root_node(graph, iter_):
    dict_root = {}
    dict_of_node_attributes = node_attributes_selection(graph, iter_)
    df_plt = pd.DataFrame(dict_of_node_attributes)
    unique, counts = np.unique(df_plt['claster_flag'], return_counts=True)
    for id_clust in unique:
        # Список узлов кластера id_clust
        list_node_clust = []
        for node in graph.nodes():
            if graph.nodes[node]['claster_flag'] == id_clust:
                list_node_clust.append(node)
        
        # Словарь узлов кластера с их bw. 
        adj_ndoes_dict_clast = {}
        # цикл по всем узлам и их смежностям
        for nb, nbrs in graph.adj.items():
            # если узел nb из числа узлов кластера id_clust
            if nb in list_node_clust:
                list_nrb = {}
                for nrb, eattr in nbrs.items():
                    # добавляем в словарь по ключу nb соседей этого узла
                    list_nrb[nrb] =  eattr
                adj_ndoes_dict_clast[nb] = list_nrb

        # рассматриваемый узел  
        for id_node in adj_ndoes_dict_clast:
            # узел сравнения 
            for id_node_2 in adj_ndoes_dict_clast:
                if id_node != id_node_2:
                    # если узел id_node имеет путь до id_node_2
                    if id_node_2 not in adj_ndoes_dict_clast[id_node]:
                        adj_ndoes_dict_clast[id_node][id_node_2] = {'weight': 100000}
                else:
                    adj_ndoes_dict_clast[id_node][id_node_2] = {'weight': 0}
        # Матрица смежности подготовлена 

        # Алгоритм
        for i in adj_ndoes_dict_clast:
            for node_1 in adj_ndoes_dict_clast:
                for nbr in adj_ndoes_dict_clast[node_1]:
                    if adj_ndoes_dict_clast[node_1][nbr]['weight'] > adj_ndoes_dict_clast[node_1][i]['weight'] + adj_ndoes_dict_clast[i][nbr]['weight']:
                        adj_ndoes_dict_clast[node_1][nbr]['weight'] = adj_ndoes_dict_clast[node_1][i]['weight'] + adj_ndoes_dict_clast[i][nbr]['weight']
        
        for node_ in adj_ndoes_dict_clast:
            eccentricity = 0
            for nrb in adj_ndoes_dict_clast[node_]:
                if adj_ndoes_dict_clast[node_][nrb]['weight'] != 100000:
                    if eccentricity < adj_ndoes_dict_clast[node_][nrb]['weight']:
                        eccentricity = adj_ndoes_dict_clast[node_][nrb]['weight']
            
        dict_root[id_clust] = {node_: eccentricity}
        
    # На данном этапе мы нашли все корневые точки Сети, по одной на кластер


# __________Создание объекта граф______________________________________
graph = nx.Graph()
# координаты центров кластеров
default_center_graphs = {}
node_generation(graph, number_of_center_nodes, number_of_nodes_in_the_cluster, default_center_graphs)

# print('Число узлов - ', len(graph_.nodes))
# print(graph_.nodes.data())
print('Количество узлов - ', len(graph.nodes))

# ____________________Запуск модели______________________
# Количество изменений координат узлов
steps = 100
while steps != 0:
    print('steps - ', steps)
    # _____Создание словаря атрибутов узлов(содержит только координаты)______
    iter_ = 0  # Число обучений алгоритма db
    dict_of_node_attributes = node_attributes_selection(graph, iter_)

    # Вывод полученых координат
    # print(dict_of_node_attributes)

    # ____________Отрисока сгенеренных узлов до обучения алгоса______________
    # G = Plot(graph, dict_of_node_attributes)
    # G.plot_graph()

    # ____________________Нахождение eps______________________________________
    # Словарь соседей для каждого узла
    dict_all_node_neighbors = finding_neighbors_of_nodes(
        graph, visibility)
    


    # #__________Подсчет средних расстояний________________
    R_nodes = сalculating_average_distances(graph, dict_all_node_neighbors, steps)

    # ____Вычисление eps по плотности узлов_____
    # Сортировка и создание списка расстояний R
    sorting_and_creating_a_list_of_distances_R(R_nodes)

    # ____________________Применяем DBSCAN___________________________________________________
    # _________Подготовка атрибутов узлов для алгоритма___________
    df = pd.DataFrame(dict_of_node_attributes)
    # print(df)
    nparr_atr_nodes = np.array(df)
    # print(nparr_atr_nodes)

    # ________обучение ____________
    db_1, iter_ = learndb(nparr_atr_nodes, eps_=60,
                          min_samples_=5, iter_=iter_)
    count_of_cluster = len(set(db_1.labels_)) - 1
    # print(count_of_cluster)
    # print(db_1.labels_)

    # ________________Отрисовка результатов первого прохода db___________
    # G_12 = Plot(graph, dict_of_node_attributes)
    # G_12.painting_of_clasters(db_1.labels_)

    # _____________Добавление узлам меток кластера_______________
    for id_node, label in enumerate(db_1.labels_):
        graph.nodes[id_node]['claster_flag'] = label

    # _________Подготовка атрибутов узлов для алгоритма_2___________

    dict_of_node_attributes_2 = node_attributes_selection(graph, iter_)
    df_2 = pd.DataFrame(dict_of_node_attributes_2)
    # print(df_2)
    nparr_atr_nodes_2 = np.array(df_2)
    # print(nparr_atr_nodes_2)

    # ________обучение ____________
    db_2, iter_ = learndb(nparr_atr_nodes_2, eps_=120,
                          min_samples_=5, iter_=iter_)

    # _____________Отрисовка результатов второго прохода db_____
    # G_22 = Plot(graph, dict_of_node_attributes_2)
    # G_22.painting_of_clasters(db_2.labels_)

    # _____________Добавление узлам меток кластера_______________
    for id_node, label in enumerate(db_2.labels_):
        if label != -1:
            graph.nodes[dict_of_node_attributes_2['id_node']
                         [id_node]]['claster_flag'] = label + count_of_cluster
        else:
            graph.nodes[dict_of_node_attributes_2['id_node']
                         [id_node]]['claster_flag'] = label

    iter_ = 0  # Закончили обучать db, обнулим iter_, чтобы отрисовывать можео было все точки

    # ___________Создание ребер между узлами___________________________________________
    edge_generation(graph, dict_all_node_neighbors, bw, visibility)

    #____________График распределения кластеров после обучения DBSCAN__________________
    dict_of_node_attributes_3 = node_attributes_selection(graph, iter_)
    df_plt = pd.DataFrame(dict_of_node_attributes_3)
    unique, counts = np.unique(df_plt['claster_flag'], return_counts=True)
    # plt.bar(unique, counts)
    # plt.title('Распределение узлов по кластерам')
    # plt.grid()
    # plt.show()

    # unique, counts = np.unique(df_plt['claster_flag'], return_counts=True)
    # print(np.asarray((unique, counts)).T) # Вывод матрицы кластеров/элементов


    # if steps == 1:
    #     G_2 = Plot(graph, dict_of_node_attributes_3)
    #     G_2.painting_of_clasters(dict_of_node_attributes_3['claster_flag'])
    # G_2 = Plot(graph, dict_of_node_attributes_3)
    # G_2.painting_of_clasters(dict_of_node_attributes_3['claster_flag'])

# ______________Отрисовка связей в графе___________________________
    # fig = plt.figure()
 
    # # syntax for 3-D projection
    # ax = plt.axes(projection ='3d')

    # iterat = 100
    # for n, nbrs in graph.adj.items():
    #     if iterat == 0:
    #         break
    #     for nbr, eattr in nbrs.items():
    #         x1 = graph.nodes[n]['x']
    #         x2 = graph.nodes[nbr]['x']
    #         y1 = graph.nodes[n]['y']
    #         y2 = graph.nodes[nbr]['y']
    #         z1 = graph.nodes[n]['z']
    #         z2 = graph.nodes[nbr]['z']
    #         ax.plot([x1, x2], [y1, y2], [z1, z2], color='b')
    #         iterat = iterat - 1
    #         if iterat == 0:
    #             break
    # plt.show()
# _____________Поиск root узлов в кластерах_____________________
    finding_root_node(graph, iter_)
# ____________________________________________________________

    shift_coord(graph, default_center_graphs)

    steps = steps - 1


