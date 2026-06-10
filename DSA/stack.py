class StackDS:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        print("Stack empty!")

    def execute(self, action, value=None):
        if action=="add":
            self.push(value)
        elif action=="remove":
            self.pop()
        elif action=="print":
            print(self.stack)
