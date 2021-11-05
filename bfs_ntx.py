import networkx as nx

num_rows = 15
num_cols = 30
graph_2d_grid = nx.grid_2d_graph(num_cols, num_rows)

import matplotlib.pyplot as plt
graph_2d_grid.pos = dict((n,n) for n in graph_2d_grid.nodes())


# nx.draw_networkx(graph_2d_grid, graph_2d_grid.pos, with_labels=False, node_size=1, font_size=4)
# plt.savefig('grid_map_1.png', dpi=300)
def y_reversed(map_size, node):
    return node[0]-1, map_size[1]-node[1]-1


map_size = (num_cols, num_rows)
start_node = y_reversed(map_size, (8, 7))
goal_node = y_reversed(map_size, (17, 2))

plt.figure(1, figsize=(12, 6))
# nx.draw_networkx(graph_2d_grid, graph_2d_grid.pos, with_labels=False, node_size=5, font_size=4)

nx.draw_networkx_nodes(graph_2d_grid,
                       graph_2d_grid.pos,
                       nodelist=graph_2d_grid.nodes,
                       node_size=355,
                       node_color='grey',
                       node_shape='s',
                       edgecolors='white')

nx.draw_networkx_nodes(graph_2d_grid,
                       graph_2d_grid.pos,
                       nodelist=[start_node],
                       node_size=155,
                       node_color='green',
                       node_shape="o"
                       )
nx.draw_networkx_nodes(graph_2d_grid,
                       graph_2d_grid.pos,
                       nodelist=[goal_node],
                       node_size=155,
                       node_color='red',
                       node_shape="*"
                       )
# plt.show()
plt.savefig('start_goal.png', dpi=400)
