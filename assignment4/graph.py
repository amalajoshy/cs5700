class Graph:
  def __init__(self, num_of_vertices):
    self._graph = []

  # function to add an edge to graph
  def add_edge(self, u, v, cost):
    self._graph.append([int(u), int(v), int(cost)])

  # The main function that finds shortest distances from src to
  # all other vertices using Bellman-Ford algorithm.
  def BellmanFord(self, src):
    # Step 1: Initialize distances from src to all other vertices
    # as INFINITE
    distance = {}
    predecessor = {}
    for u, v, cost in self._graph:
      distance[u] = float('inf')
      distance[v] = float('inf')

    distance[src] = 0

    # Step 2: Relax all edges |V| - 1 times. A simple shortest
    # path from src to any other vertex can have at-most |V| - 1
    # edges
    for i in range(len(distance) - 1):
      # Update dist value and parent index of the adjacent vertices of
      # the picked vertex. Consider only those vertices which are still in
      # queue
      for u, v, cost in self._graph:
        if distance[u] != float('inf') and distance[u] + cost < distance[v]:
          distance[v] = distance[u] + cost
          predecessor[v] = u

    # We can skip step 3 because we are expecting only positive integer weights/cost

    entries = []
    for dest in distance:
      next_hop = self._get_next_hop(src, dest, predecessor)
      if next_hop is not None:
        entries.append((dest, next_hop, distance[dest]))
    return entries

  def _get_next_hop(self, src, dest, predecessor):
    next_hop = dest
    while next_hop in predecessor and predecessor[next_hop] != src:
      next_hop = predecessor[next_hop]
    if next_hop in predecessor:
      return next_hop
    else:
      return None
