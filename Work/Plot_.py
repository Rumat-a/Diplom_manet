import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt


class Plot:
    def __init__(self, graph,  dict_of_node_attributes):
        self.__graph = graph # Мб пригодится в будущем
        self.__dict_of_node_attributes = dict_of_node_attributes

    def plot_graph(self):
        # Создаем трехмерную фигуру
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        x = self.__dict_of_node_attributes['x']
        y = self.__dict_of_node_attributes['y']
        z = self.__dict_of_node_attributes['z']    
        claster_flag = self.__dict_of_node_attributes['claster_flag']
        # ax.scatter(x, y, z, c = claster_flag, s=20, cmap=plt.cm.Spectral)

        # Получаем уникальные значения кластеров, исключая -1
        unique_clusters = set([cluster for cluster in claster_flag if cluster != -1])
        # Создаем палитру цветов с использованием уникальных значений кластеров
        colors = [plt.cm.jet(float(i) / max(unique_clusters)) for i in unique_clusters]
        # Создаем словарь, сопоставляющий каждому кластеру его цвет
        cluster_color_dict = {cluster: color for cluster, color in zip(unique_clusters, colors)}
        # Добавляем цвет для кластера -1
        cluster_color_dict[-1] = 'black'
        # Получаем список цветов для каждого кластера
        cluster_colors = [cluster_color_dict[cluster] for cluster in claster_flag]

        ax.scatter(x, y, z, c=cluster_colors, s=20)


        plt.title('Дефолт')
        plt.xlabel('Ось Х')
        plt.ylabel('Ось Y')
        plt.show()


    def painting_of_clasters(self, dbscan_label):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        x = self.__dict_of_node_attributes['x']
        y = self.__dict_of_node_attributes['y']
        z = self.__dict_of_node_attributes['z']

        unique_clusters = set([cluster_flag for cluster_flag in dbscan_label if cluster_flag != -1])
        # Создаем палитру цветов с использованием уникальных значений кластеров
        colors = [plt.cm.jet(float(i) / max(unique_clusters)) for i in unique_clusters]
            # используется функция plt.cm.jet, которая представляет собой палитру цветов Jet (градиент от голубого до красного).
            # float(i) / max(unique_clusters) выполняет нормализацию значения i в диапазоне от 0 до 1.
        # Создаем словарь, сопоставляющий каждому кластеру его цвет
        cluster_color_dict = {cluster_flag: color for cluster_flag, color in zip(unique_clusters, colors)}
        # Добавляем цвет для кластера -1
        cluster_color_dict[-1] = 'black'
        # Получаем список цветов для каждого кластера
        cluster_colors = [cluster_color_dict[cluster_flag] for cluster_flag in dbscan_label]

        ax.scatter(x, y, z, c=cluster_colors, s=20)     

        plt.title('Кластеризация узлов сети')
        plt.xlabel('Ось Х')
        plt.ylabel('Ось Y')
        plt.show()
    