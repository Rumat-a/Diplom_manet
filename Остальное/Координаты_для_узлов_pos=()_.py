import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_node(1, pos=(0, 0))
G.add_node(2, pos=(1, 1))
G.add_node(3, pos=(2, 0))

pos = nx.get_node_attributes(G, 'pos')

nx.draw(G, pos, with_labels=True)

plt.show()