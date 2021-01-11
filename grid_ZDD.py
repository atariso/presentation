from graphillion import GraphSet
import graphillion.tutorial as tl

n = 8

universe = tl.grid(n, n)
GraphSet.set_universe(universe)
tl.draw(universe)

start = 1
goal = (n + 1) ** 2

paths = GraphSet.paths(start, goal)
print(len(paths))
