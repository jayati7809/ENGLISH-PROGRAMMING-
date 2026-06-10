class QueueDS:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        print("Queue empty!")

    def execute(self, action, value=None):
        if action=="add":
            self.enqueue(value)
        elif action=="remove":
            self.dequeue()
        elif action=="print":
            print(self.queue)
