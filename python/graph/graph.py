from collections import deque

class Graph:
    """
    Simple graph using adjacency list.
    - directed: if True, edges are one-way
    - if False, edges are added both directions (undirected)
    """
    def __init__(self, directed=False):
        self.directed = directed
        self.adj = {}  # node -> list of neighbors

    def add_node(self, node):
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, u, v):
        self.add_node(u)
        self.add_node(v)

        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)

    def bfs(self, start):
        if start not in self.adj:
            return []

        visited = set()
        order = []
        q = deque()

        visited.add(start)
        q.append(start)

        while q:
            node = q.popleft()
            order.append(node)

            for nei in self.adj[node]:
                if nei not in visited:
                    visited.add(nei)
                    q.append(nei)

        return order

    def dfs(self, start):
        if start not in self.adj:
            return []

        visited = set()
        order = []

        def helper(node):
            visited.add(node)
            order.append(node)
            for nei in self.adj[node]:
                if nei not in visited:
                    helper(nei)

        helper(start)
        return order


if __name__ == "__main__":
    g = Graph(directed=False)
    edges = [(1, 2), (1, 3), (2, 4), (3, 5)]
    for u, v in edges:
        g.add_edge(u, v)

    print("Adjacency list:", g.adj)
    print("BFS from 1:", g.bfs(1))
    print("DFS from 1:", g.dfs(1))
