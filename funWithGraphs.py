#!/usr/bin/python

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#tet = nx.tetrahedral_graph()
#nx.draw(tet)
#plt.show()

#red = nx.random_lobster(100, 0.9, 0.9)
#nx.draw(red)
#plt.show()

G = nx.random_geometric_graph(200, 0.125)
pos = nx.get_node_attributes(G, 'pos')

dmin = 1
ncenter = 0
for n in pos:
    x,y = pos[n]
    d = (x-0.5)**2 + (y-0.5)**2
    if d < dmin:
        ncenter = n
        dmin = d

print ncenter
p = nx.single_source_shortest_path_length(G, ncenter)
print p

nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
nx.draw_networkx_nodes(G, pos, nodelist=p.keys(), node_size=80, node_color=p.values(), cmap=plt.cm.Reds_r)

plt.xlim(-0.05, 1.05)
plt.ylim(-0.05, 1.05)
plt.axis('off')
plt.show()
