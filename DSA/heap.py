import heapq

class HeapDS:
    def __init__(self):
        self.heap = []

    def insert(self,value):
        heapq.heappush(self.heap,value)

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)
        print("Heap empty!")

    def print(self):
        print(self.heap)

    def execute(self, action, value=None):
        if action=="add":
            self.insert(value)
        elif action=="remove":
            self.pop()
        elif action=="print":
            self.print()
