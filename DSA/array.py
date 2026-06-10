class ArrayDS:
    def __init__(self, size=10):
        self.size = size
        self.array = [0]*size
        self.index = 0

    def add(self, value):
        if self.index < self.size:
            self.array[self.index] = value
            self.index += 1
        else:
            print("Array full!")

    def print(self):
        print(self.array[:self.index])

    def execute(self, action, value=None):
        if action=="add":
            self.add(value)
        elif action=="print":
            self.print()
