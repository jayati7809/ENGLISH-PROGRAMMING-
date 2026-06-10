class ListDS:
    def __init__(self):
        self.list = []

    def append(self, value):
        self.list.append(value)

    def sort(self):
        self.list.sort()

    def sum(self):
        return sum(self.list)

    def execute(self, action, value=None):
        if action=="add":
            self.append(value)
        elif action=="sort":
            self.sort()
        elif action=="sum":
            return self.sum()
        elif action=="print":
            print(self.list)
