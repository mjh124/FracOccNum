#!/usr/bin/python

#nodes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
#distances = {
#    'B': {'A': 5, 'D': 1, 'G': 2},
#    'A': {'B': 5, 'D': 3, 'E': 12, 'F' :5},
#    'D': {'B': 1, 'G': 1, 'E': 1, 'A': 3},
#    'G': {'B': 2, 'D': 1, 'C': 2},
#    'C': {'G': 2, 'E': 1, 'F': 16},
#    'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
#    'F': {'A': 5, 'E': 2, 'C': 16}}

nodes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
distances = {'0': {'1':1, '3':1, '5':1, '7':1, '11':1, '12':1, '13':1}, 
             '1': {'0':1, '3':1, '7':1, '10':1, '11':1, '14':1}, 
             '2': {'3':1, '4':1, '6':1, '8':1, '10':1, '14':1}, 
             '3': {'0':1, '1':1, '2':1, '4':1, '6':1, '7':1, '8':1, '10':1, '11':1, '12':1, '13':1, '14':1}, 
             '4': {'2':1, '3':1, '7':1, '8':1, '9':1, '10':1, '13':1}, 
             '5': {'0':1, '7':1, '9':1, '13':1}, 
             '6': {'2':1, '3':1, '8':1, '11':1, '12':1, '14':1}, 
             '7': {'0':1, '1':1, '3':1, '4':1, '5':1, '9':1, '10':1, '13':1}, 
             '8': {'2':1, '3':1, '4':1, '6':1, '12':1, '13':1}, 
             '9': {'4':1, '5':1, '7':1, '13':1}, 
            '10': {'1':1, '2':1, '3':1, '4':1, '7':1, '14':1}, 
            '11': {'0':1, '1':1, '3':1, '6':1, '12':1, '14':1}, 
            '12': {'0':1, '3':1, '6':1, '8':1, '11':1, '13':1}, 
            '13': {'0':1, '3':1, '4':1, '5':1, '7':1, '8':1, '9':1, '12':1}, 
            '14': {'1':1, '2':1, '3':1, '6':1, '10':1, '11':1}}
#
#for atom, neighbor in neighbors.items():
#    if neighbor not in unvisited: continue
#    newDistance = currentDistance + 1
#    if unvisited[atom] is None or unvisited[atom] > newDistance:
#        unvisited[atom] = newDistance
#visited[current] = currentDistance
#del unvisited[current]
#if not unvisited: break
#candidates = [node for node in unvisited.items() if node[1]]
#current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]

unvisited = {node: None for node in nodes} #using None as +inf
visited = {}
current = '0' #source
currentDistance = 0
unvisited[current] = currentDistance #Set from source to itself as 0

while True:
    for neighbour, distance in distances[current].items():
        if neighbour not in unvisited: continue
        newDistance = currentDistance + distance
        if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
            unvisited[neighbour] = newDistance
    visited[current] = currentDistance
    del unvisited[current]
    if not unvisited: break
    candidates = [node for node in unvisited.items() if node[1]]
    current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]

print(visited)
