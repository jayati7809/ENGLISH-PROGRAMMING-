class GraphDS:
    def __init__(self):
        self.graph = {}

    def add_edge(self,u,v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def add_weighted_edge(self,edge):
        u,v,w = edge
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v,w))

    def print(self):
        print(self.graph)

    def execute(self, action, value=None):
        if action=="add_edge":
            self.add_edge(*value)
        elif action=="add_weighted_edge":
            self.add_weighted_edge(value)
        elif action=="print":
            self.print()
