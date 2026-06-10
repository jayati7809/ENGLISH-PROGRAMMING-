from engine.nlp_parser import extract_action_entities

class FunctionRegistry:
    def __init__(self):
        self.functions = {}
        self.executor = None

    def define(self, name, args, body_lines):
        self.functions[name] = (args, body_lines)
        print(f"Function '{name}' defined with args {args}")

    def call(self, name, arg_values):
        if name not in self.functions:
            print(f"Function '{name}' not found")
            return
        args, body_lines = self.functions[name]
        if len(args) != len(arg_values):
            print(f"Function '{name}' expects {len(args)} args")
            return
        local_vars = self.executor.vars.objects.copy()
        for i,arg in enumerate(args):
            local_vars[arg] = arg_values[i]
        for line in body_lines:
            concepts = extract_action_entities(line)
            if "numbers" in concepts:
                concepts["numbers"] = [local_vars.get(n,n) for n in concepts["numbers"]]
            if "name" in concepts and concepts["name"] in local_vars:
                concepts["name"] = local_vars[concepts["name"]]
            self.executor.execute(concepts)
