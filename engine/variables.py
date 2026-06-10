class VariableTable:
    def __init__(self):
        self.objects = {}
        self.current = None

    def set(self, name, obj):
        self.objects[name] = obj
        self.current = obj

    def get(self, name):
        return self.objects.get(name)
