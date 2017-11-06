#!/usr/bin/python

import numpy as np
import networkx as nx
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl

if len(sys.argv) != 4:
    print "AuNC_RadAng_Topology.py fn-xyz start-radius end-radius"
    print " Probably eventually include analysis of SuperAtom DOS"
    exit(0)

fn_xyz = sys.argv[1]
start_rad = float(sys.argv[2])
end_rad = float(sys.argv[3])

def parse_byElem(fn_xyz, elem):

    x = []
    y = []
    z = []
    with open(fn_xyz, 'r') as f:
        lines = f.readlines()[2:]
        for line in lines:
            tokens = line.split()
            if tokens[0] == elem:
                x.append(float(tokens[1]))
                y.append(float(tokens[2]))
                z.append(float(tokens[3]))
    return x, y, z

def parse_byRad(fn_xyz, cut_range, center):

    sym = []
    x = []
    y = []
    z = []
    start = cut_range[0]
    end = cut_range[1]
    with open(fn_xyz, 'r') as f:
        lines = f.readlines()[2:]
        for line in lines:
            tokens = line.split()
            point = np.array([float(tokens[1]), float(tokens[2]), float(tokens[3])])
            dist = distance(center, point)
            if tokens[0] == 'H' or tokens[0] == 'C':
                continue
            if dist > start and dist < end:
                sym.append(tokens[0])
                x.append(float(tokens[1]))
                y.append(float(tokens[2]))
                z.append(float(tokens[3]))
    return sym, x, y, z

def get_RadiusofCircumscribedCircle(center, x, y, z):

    CC_rad = 0.0
    center_atom_dist = 5.0
    for i in range(len(x)):
        point = np.array([x[i], y[i], z[i]])
        dist = distance(center, point)
        if dist > CC_rad:
            CC_rad = dist
        if dist < center_atom_dist:
            center_atom_dist = dist
            center_atom_idx = i
    return CC_rad, center_atom_idx

def make_radial_slice(center, x, y, z, cut_range):

    idx_inSlice = []
    for i in range(len(x)):
        point = np.array([x[i], y[i], z[i]])
        dist = distance(center, point)
        if dist > cut_range[0] and dist < cut_range[1]:
            idx_inSlice.append(i)
    return idx_inSlice

def build_adjMat_EuclideanDistMat(x, y, z, thres):

    Natoms = len(x)
    AdjMat = np.zeros((Natoms, Natoms))
    DistEuclid = np.zeros((Natoms, Natoms))
    for i in range(Natoms):
        point1 = np.array([x[i], y[i], z[i]])
        for j in range(Natoms):
            point2 = np.array([x[j], y[j], z[j]])
            dist = distance(point1, point2)
            DistEuclid[i][j] = dist
            if 0.0 < dist < thres:
                AdjMat[i][j] = 1
    return AdjMat, DistEuclid

def parse_AdjMat(AdjMat):

    CEs = {}
    for i in range(len(AdjMat)):
        CE_i = []
        for j in range(len(AdjMat)):
            if AdjMat[i][j] == 1:
                CE_i.append(str(j))
        CEs[str(i)] = CE_i
    return CEs

def get_CoordEnv_withWeight(x, y, z, atom_idx, thres):

    CoordEnv = {}
    point1 = np.array([x[atom_idx], y[atom_idx], z[atom_idx]])
    for i in range(len(x)):
        point2 = np.array([x[i], y[i], z[i]])
        dist = distance(point1, point2)
        if 0.0 < dist < thres:
            CoordEnv[str(i)] = 1 # Change here to make weighted graph
    return CoordEnv

def get_Dijkstra_dist(source, nodes, neighbors):

    unvisited = dict.fromkeys(nodes, None)
    visited = {}
    current = source
    currentDistance = 0
    unvisited[current] = currentDistance

    while True:
        for neighbor, distance in neighbors[current].items():
            if neighbor not in unvisited: continue
            newDistance = currentDistance + distance
            if unvisited[neighbor] is None or unvisited[neighbor] > newDistance:
                unvisited[neighbor] = newDistance
        visited[current] = currentDistance
        del unvisited[current]
        if not unvisited: break
        candidates = [node for node in unvisited.items() if node[1]]
        current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]
    return visited

def calc_DistMat(x, y, z, thres):

    Natoms = len(x)
    DistMat = np.zeros((Natoms, Natoms))
    CE = {}
    nodes = []
    for i in range(Natoms):
        nodes.append(str(i))
        CoordEnv = get_CoordEnv_withWeight(x, y, z, i, thres)
        CE[str(i)] = CoordEnv
    for i in range(Natoms):
        bond_dist = get_Dijkstra_dist(str(i), nodes, CE)
        for j in bond_dist:
            DistMat[i][int(j)] = bond_dist[j]
    return DistMat

def calc_WienerNumber(DistMat):

    wiener = 0
    for i in range(len(DistMat)):
        for j in range(len(DistMat)):
            wiener += DistMat[i][j]
    return wiener / 2

def BL_to_CN(BL, BL_eq, BL_sig):
    return np.exp(-((BL-BL_eq)/BL_sig)**2)

def distance(point1, point2):
    return np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2 + (point1[2]-point2[2])**2)
    
def get_rowSum(mat, i):
    # Use this to get atomic wiener index
    return sum(mat[i])

def generate_edges(graph):
    # Generates a list of tuples that represent the nodes an edge connects
    edges = []
    for node in graph:
        for neighbor in graph[node]:
            edges.append((node, neighbor))
    return edges

def plot_histogram(data, Nbins, cumulative=0):

    n, bins, patches = plt.hist(data, Nbins, normed=0, facecolor='g', cumulative=cumulative, alpha=0.75)
    #n1, bins1, patches1 = plt.hist(data, Nbins, normed=1, facecolor='b', cumulative=1, histtype='step', alpha=0.75)
    
    x_min = data.min() - 1
    x_max = data.max() + 1
    y_min = 0
    y_max = n.max() + (n.max()*.1)
    plt.axis([x_min, x_max, y_min, y_max])

    plt.xlabel('Wiener Number')
    plt.ylabel('Count (# Atoms)')
    #plt.ylabel('Count (# Atoms)')
    #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    plt.grid(True)
    plt.show()

#def plot_graph(AdjMat, DistEuclid, center_atom_idx, color_data):
def plot_graph(AdjMat, DistEuclid, color_data):

    """
       AdjMat - Adjacency matrix for a graph
       DistEuclid - The euclidean distance matrix for a spatial graph - not currently required, could for edge weights
       center_atom_idx - index of atom in the center
       color_data - array of numerical data of length #Nodes, to color the nodes by (node to value dict built within)
    """

    graph = nx.Graph() # Initialize empty graph

    # Add all nodes and edges, including attributes of each
    CEs = parse_AdjMat(AdjMat)
    for i in CEs:
        graph.add_node(i, element='Au') #Generalize this
        for j in CEs[i]:
            dist = DistEuclid[int(i)][int(j)]
            graph.add_edge(i, j, weight=dist)
    #print graph.nodes(data=True)
    #print graph.edges(data=True)

    pos = nx.spring_layout(graph)

    p = {}
    for i in range(len(color_data)):
        p[str(i)] = color_data[i]
    #p = nx.single_source_shortest_path_length(graph, str(center_atom_idx))

    elem = nx.get_node_attributes(graph, 'element') #Not used
    nx.draw_networkx_edges(graph, pos, alpha=1.0)
    #nx.draw_networkx_edges(graph, pos, nodelist=[str(center_atom_idx)], alpha=1.0)
    nx.draw_networkx_nodes(graph, pos, nodelist=p.keys(), node_size=150, node_color=p.values(), cmap=mpl.cm.Reds)
    plt.show()
    #plt.savefig("graph.png")

def build_colorbar(color_data):

    fig = plt.figure()
    ax = fig.add_axes([0.05, 0.05, 0.2, 0.9])
    cmap = mpl.cm.Reds
    norm = mpl.colors.Normalize(vmin=color_data.min(), vmax=color_data.max())
    bounds = np.linspace(color_data.min(), color_data.max(), 10)
    cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation='vertical', ticks=bounds)
    cb1.set_label('Wiener Number')
    plt.show()

if __name__ == "__main__":

    ###
    # System Setup
    ###

    thres = 3.5 # Distance threshold to define a bond
    cut_range = [start_rad, end_rad] # Do cut from initial parse, if need to plot something based on cut radius...change later
    #cut_range = [4.0, 7.0]

    Au_x, Au_y, Au_z = parse_byElem(fn_xyz, 'Au')
    #S_x, S_y, S_z = parse_byElem(fn_xyz, 'S', cut_range)
    center = np.array([np.average(Au_x), np.average(Au_y), np.average(Au_z)])

    sym, x, y, z = parse_byRad(fn_xyz, cut_range, center)
    for i in range(len(sym)):
        print sym[i], x[i], y[i], z[i]

    #CC_rad, center_atom_idx = get_RadiusofCircumscribedCircle(center, Au_x, Au_y, Au_z) # This is closest to the center, if no direct center atom, some essentially random one will be found
    #print CC_rad, center_atom_idx # CC_rad will probably only be useful if whole particle is considered
    #idx_inSlice = make_radial_slice(center, Au_x, Au_y, Au_z, cut_range)
    #for i in range(len(x)):
    #    print x[i], y[i], z[i]

    ###
    # Topology
    ###

    AdjMat, DistEuclid = build_adjMat_EuclideanDistMat(x, y, z, thres)
    DistMat = calc_DistMat(x, y, z, thres)
    wiener = calc_WienerNumber(DistMat)
    print wiener
    WNs = []
    for i in range(len(sym)):
        WNs.append(get_rowSum(DistMat, i)) #Row sum of Distance matrix is the wiener number of that atom
    print WNs
    plot_histogram(np.asarray(WNs), 20)
    #plot_histogram(np.asarray(WNs), 10, 1)  #Will plot cumulative distribtuion of WNs

    # Truncate AdjMat, DistMat, and DistEuclid based on which indices are in the slice?

    plot_graph(AdjMat, DistEuclid, np.asarray(WNs))
    #plot_graph(AdjMat, DistEuclid, center_atom_idx, np.asarray(WNs))
    #build_colorbar(np.asarray(WNs))
