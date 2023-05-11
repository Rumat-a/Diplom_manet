import networkx as nx
import random
import matplotlib.pyplot as plt
random.seed(123)


def gen_nodes_metrics():  # Функция для создания метрик для узла
    # Список всех узлов, где node_id - имя узла, а {атрибуты по ключу}
    node_list = []
    i = 0
    while len(node_list) != 100:  # Создаем 100 узлов
        i += 1
        node_id = i
        # neighbor_1 = random.randint(0, 100)
        # neighbor_2 = random.randint(0, 100)
        # (neighbor_1, neighbor_2)
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        z = random.uniform(0, 1000)
        node_list.append(
            (node_id, {'x': x, 'y': y, 'z': z}))
    return node_list

# Это работа алгоритма кластеризации
# def gen_edges_for_graph(node_list):
#     # Степень вершины - это количество ребер, связывающих данную вершину с другими вершинами графа.
#     node_degree = random.randint(0, 10)
#     edges_list = []
#     for i in range(node_list):
#          print(i)


# Список узлов
node_list = list(tuple(dict()))
node_list = gen_nodes_metrics()
# print(random.choice(node_list))
# print('len(node_list) - ', len(node_list))

# Генерация пустого графа
G = nx.Graph()

# Добваление узлов в граф (Graph with 100 nodes and 0 edges)
G.add_nodes_from(node_list)
# print('len(G) - ',len(G))
# print(G.nodes.data())

# # Список ребер
# edges_list = list(tuple())
# edges_list = gen_edges_for_graph(node_list)


# Graph with 10 nodes and 9 edges
h = nx.path_graph(10)
# print(h.edges)

# Отображаем граф
# plt.show()

# print('h.adj[1] - ', h.adj[4])
# # График
# # with_labels=True говорит библиотеке отображать номера узлов на графе. font_weight='bold' используется для увеличения жирности шрифта номеров узлов.
# nx.draw(h, with_labels=True, font_weight='bold')
# plt.show()


# Очищает все данные графа
G.clear()
# print(G.nodes, G.edges)

G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')
# Graph with 8 nodes and 3 edges
# print(G)
# print(G.number_of_nodes(),
#       G.number_of_edges()
#       )


DG = nx.DiGraph()
DG.add_edge(2, 1)   # adds the nodes in order 2, 1
DG.add_edge(1, 3)
DG.add_edge(2, 4)
DG.add_edge(1, 2)
assert list(DG.successors(2)) == [1, 4]
assert list(DG.edges) == [(2, 1), (2, 4), (1, 3), (1, 2)]
