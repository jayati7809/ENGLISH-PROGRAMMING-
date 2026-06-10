class BSTNode:
    def __init__(self,val):
        self.val = val
        self.left = None
        self.right = None

class BSTDS:
    def __init__(self):
        self.root = None

    def insert_node(self,node,val):
        if not node:
            return BSTNode(val)
        if val<node.val:
            node.left = self.insert_node(node.left,val)
        else:
            node.right = self.insert_node(node.right,val)
        return node

    def insert(self,val):
        self.root = self.insert_node(self.root,val)

    def inorder(self,node,res):
        if node:
            self.inorder(node.left,res)
            res.append(node.val)
            self.inorder(node.right,res)
        return res

    def print(self):
        print(self.inorder(self.root,[]))

    def execute(self, action, value=None):
        if action=="add":
            self.insert(value)
        elif action=="print":
            self.print()
