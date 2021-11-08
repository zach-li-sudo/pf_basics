# ----> dij_astar_speed_compare.py
import networkx as nx
import matplotlib.pyplot as plt
from time import time
import pandas as pd
import numpy as np


def dji_astar_elapse_time(size_array):
    # df = pd.DataFrame()
    data = []
    for s in size_array:
        num_rows, num_cols = s, s
        graph_2d_grid = nx.grid_2d_graph(num_cols, num_rows)
        graph_2d_grid.pos = dict((n,n) for n in graph_2d_grid.nodes())

        start_node = (0, 2)
        goal_node = (num_cols-3, num_rows-3)

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
        shortest_path_Dijk = nx.dijkstra_path(graph_2d_grid, 
                                        source=start_node, 
                                        target=goal_node)
        dist_Dijk = nx.dijkstra_path_length(graph_2d_grid, 
                                    source=start_node, 
                                    target=goal_node)

        td = time() - td

        edges_Dijk = []
        for i in range(len(shortest_path_Dijk) - 1):
            current_node = shortest_path_Dijk[i]
            next_node = shortest_path_Dijk[i+1]
            edges_Dijk.append((current_node, next_node))


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
        data.append([s, round(td, 5), round(ta, 5)])
    
    data = np.asarray(data)

    df = pd.DataFrame(data, columns=["mapSize", "Dijk", "A*"])
    return df



if __name__ == "__main__":
    size_array = [s for s in range(20, 200, 40)]
    size_array += [200, 300, 400, 500]
    
    df = dji_astar_elapse_time(size_array)
    print(df)

    ax = plt.gca()
    df.plot(kind='scatter', x='mapSize', y='Dijk', ax=ax)
    df.plot(kind='scatter', x='mapSize', y='A*', color='red', ax=ax)
    
    plt.ylabel('Elapse time/s')
    plt.title("Comparison of speed Dijkstra/A*")
    plt.legend(['Dijk', 'A*'])
    plt.savefig('comp_dij_astar.png', dpi=400)
    plt.show()
