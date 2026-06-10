class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class LinkedListDS:
    def __init__(self):
        self.head = None

    def insert(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def print(self):
        vals = []
        cur = self.head
        while cur:
            vals.append(cur.val)
            cur = cur.next
        print(vals)

    def execute(self, action, value=None):
        if action=="add":
            self.insert(value)
        elif action=="print":
            self.print()
