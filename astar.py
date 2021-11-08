# A star heuristic
import networkx as nx
import matplotlib.pyplot as plt
from time import time

num_rows = 15
num_cols = 15
graph_2d_grid = nx.grid_2d_graph(num_cols, num_rows)
graph_2d_grid.pos = dict((n,n) for n in graph_2d_grid.nodes())

start_node = (0, 2)
goal_node = (11, 13)


# obstacles
obstacles = []
for x in range(2, 13):
    y = 2
    nd = (x, y)
    obstacles.append(nd)

for x in range(5, 12):
    y = 12
    nd = (x, y)
    obstacles.append(nd)

for y in range(2, 13):
    x = 12
    nd = (x, y)
    obstacles.append(nd)

# remove obstacle nodes in map
graph_2d_grid.remove_nodes_from(obstacles)


# find shortest path dijkstra
td = time()
shortest_path_djik = nx.dijkstra_path(graph_2d_grid, 
                                 source=start_node, 
                                 target=goal_node, 
                                 weight='weight')
dist_djik = nx.dijkstra_path_length(graph_2d_grid, 
                               source=start_node, 
                               target=goal_node, 
                               weight='weight')

td = time() - td

edges_djik = []
for i in range(len(shortest_path_djik) - 1):
    current_node = shortest_path_djik[i]
    next_node = shortest_path_djik[i+1]
    edges_djik.append((current_node, next_node))



# A star heuristic
def my_heuristic(source, target):
    return abs(source[0] - target[0]) + abs(source[1] - target[1])

ta = time()
shortest_path_astar = nx.astar_path(graph_2d_grid, 
                                 source=start_node, 
                                 target=goal_node,
                                 heuristic= my_heuristic)

dist_astar = nx.astar_path_length(graph_2d_grid, 
                                 source=start_node, 
                                 target=goal_node,
                                 heuristic= my_heuristic)

ta = time() - ta


edges_astar = []
for i in range(len(shortest_path_astar) - 1):
    current_node = shortest_path_astar[i]
    next_node = shortest_path_astar[i+1]
    edges_astar.append((current_node, next_node))




from copy import deepcopy
# path graph

path_graph_djik = deepcopy(graph_2d_grid)
other_nodes_djik = []
for node in path_graph_djik.nodes:
    if node not in shortest_path_djik[1:-1]:
        other_nodes_djik.append(node)

path_graph_djik.remove_nodes_from(other_nodes_djik)


path_graph_astar = deepcopy(graph_2d_grid)
other_nodes_astar = []
for node in path_graph_astar.nodes:
    if node not in shortest_path_astar[1:-1]:
        other_nodes_astar.append(node)

path_graph_astar.remove_nodes_from(other_nodes_astar)



if num_cols >= 100 or num_rows >= 100:
    print('Djikstra time: {}, A star time: {}'.format(td, ta))
    exit()

plt.figure(figsize=(12, 6))
ax1 = plt.subplot(1, 2, 1)
nx.draw_networkx_nodes(graph_2d_grid, 
                       graph_2d_grid.pos, 
                       node_size=375,
                       node_color='grey',
                       node_shape='s',
                       edgecolors='white')

nx.draw_networkx_nodes(path_graph_djik, 
                       path_graph_djik.pos,
                       node_shape='o',
                       node_color='r',
                       node_size=200)

nx.draw_networkx_edges(path_graph_djik, 
                       path_graph_djik.pos, 
                       edgelist=edges_djik, 
                       edge_color='red', 
                       width=5)

nx.draw_networkx_nodes(graph_2d_grid, 
                       graph_2d_grid.pos, 
                       nodelist=[start_node], 
                       node_color='pink',
                       node_shape='*',
                       node_size=590)

nx.draw_networkx_nodes(graph_2d_grid, 
                       graph_2d_grid.pos, 
                       nodelist=[goal_node], 
                       node_color='green',
                       node_shape='X',
                       node_size=590)

ax1.title.set_text('Djikstra distance={}\n elapse time={}'.format(dist_djik, td))


ax2 = plt.subplot(1, 2, 2)
nx.draw_networkx_nodes(graph_2d_grid, 
                       graph_2d_grid.pos, 
                       node_size=375,
                       node_color='grey',
                       node_shape='s',
                       edgecolors='white')

nx.draw_networkx_nodes(path_graph_astar, 
                       path_graph_astar.pos,
                       node_shape='o',
                       node_color='lightyellow',
                       node_size=200)

nx.draw_networkx_edges(path_graph_astar, 
                       path_graph_astar.pos, 
                       edgelist=edges_astar, 
                       edge_color='red', 
                       width=5)

nx.draw_networkx_nodes(graph_2d_grid, 
                       graph_2d_grid.pos, 
                       nodelist=[start_node], 
                       node_color='pink',
                       node_shape='*',
                       node_size=590)

nx.draw_networkx_nodes(graph_2d_grid, 
                       graph_2d_grid.pos, 
                       nodelist=[goal_node], 
                       node_color='green',
                       node_shape='X',
                       node_size=590)

ax2.title.set_text('A star distance={}\n elapse time={}'.format(dist_astar, ta))
# plt.show()
plt.savefig('djikstra_astar.png', dpi=400)
exit()