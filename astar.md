### A\* Algorithm

> Dijkstra's Algorithm works well to find the shortest path, but it wastes time exploring in directions that are not promising. Greedy Best First Search explores in promising directions but it may not find the shortest path. The A* algorithm uses *both\* the actual distance from the start and the estimated distance to the goal.
>
> ---- Introduction to the A\* Algorithm, [Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html#breadth-first-search)

Different from the Dijkstra's Algorithm, A star uses a heuristic to render the nodes, such that the exploring frontier expands towards the goal, rather than explores in all directions like the Dijkstra's algorithm. So A star is more likely to be faster especially in large scale and complex graphs.

```python
def heuristic(source, target):
		return abs(source[0]-target[0]) + abs(source[1]-target[1])
```

In this section, we first check the optimality of A* algorithm, then we perform Dijkstra's algorithm and A* algorithm in different map sizes to compare their performance.

- A\* path and Dijkstra Path
  Create a $15\times15$ map to implement the algorithms.

```python
########## ---->  astar.py
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
shortest_path_Dijk = nx.dijkstra_path(graph_2d_grid,
                                source=start_node,
                                target=goal_node,
                                weight='weight')
dist_Dijk = nx.dijkstra_path_length(graph_2d_grid,
                                source=start_node,
                                target=goal_node,
                                weight='weight')
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

edges_astar = []
for i in range(len(shortest_path_astar) - 1):
    current_node = shortest_path_astar[i]
    next_node = shortest_path_astar[i+1]
    edges_astar.append((current_node, next_node))
```

Here we use `time()` function to find out the elapse time of the two algorithm.

```python
###### ---->  astar.py
...
from copy import deepcopy
###### path graph
path_graph_Dijk = deepcopy(graph_2d_grid)
other_nodes_Dijk = []
for node in path_graph_Dijk.nodes:
    if node not in shortest_path_Dijk[1:-1]:
        other_nodes_Dijk.append(node)

path_graph_Dijk.remove_nodes_from(other_nodes_Dijk)


path_graph_astar = deepcopy(graph_2d_grid)
other_nodes_astar = []
for node in path_graph_astar.nodes:
    if node not in shortest_path_astar[1:-1]:
        other_nodes_astar.append(node)

path_graph_astar.remove_nodes_from(other_nodes_astar)



if num_cols >= 100 or num_rows >= 100:
    print('Dijkstra time: {}, A star time: {}'.format(td, ta))
    exit()

plt.figure(figsize=(12, 6))
ax1 = plt.subplot(1, 2, 1)
nx.draw_networkx_nodes(graph_2d_grid,
                       graph_2d_grid.pos,
                       node_size=375,
                       node_color='grey',
                       node_shape='s',
                       edgecolors='white')

...

ax1.title.set_text('Dijkstra distance={}\n elapse time={}'.format(dist_Dijk, td))

ax2 = plt.subplot(1, 2, 2)
nx.draw_networkx_nodes(graph_2d_grid,
                       graph_2d_grid.pos,
                       node_size=375,
                       node_color='grey',
                       node_shape='s',
                       edgecolors='white')
...
ax2.title.set_text('A star distance={}\n elapse time={}'.format(dist_astar, ta))
# plt.show()
plt.savefig('dijkstra_astar.png', dpi=400)
```

Compare the paths and elapse time:

![img](https://github.com/zach-li-sudo/pf_basics/dijkstra_astar.png)

We can see that the two optimal paths are identical, implying the optimality of A star. But the elapse time of Dijkstra is smaller than A star, which seems to contradict with our claim. The reason is that the map size is not large enough for A star to show its privileges to the Dijkstra's method.

```python
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
```

Run this code we can get the terminal prints and the scatter plot:

```bash
	 mapSize      Dijk       A*
0     20.0   0.01397  0.00886
1     60.0   0.05075  0.09842
2    100.0   0.10722  0.12561
3    140.0   0.28358  0.27283
4    180.0   0.50350  0.46888
5    200.0   0.99292  0.56150
6    300.0   3.13766  1.34420
7    400.0   7.79042  2.47135
8    500.0  14.40311  5.41550
```

![comp](https://github.com/zach-li-sudo/pf_basics/comp_dij_astar.png)

When the map size is small or medium $(\le200)$, the two algorithms has the similar performance. But A star is way faster when the map size becomes large. The trend confirms our claim at the very beginning of this section.
