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