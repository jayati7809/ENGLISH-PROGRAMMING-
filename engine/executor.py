from engine.registry import DSA_TYPES
from engine.variables import VariableTable
from engine.functions import FunctionRegistry
from engine.nlp_parser import extract_action_entities

class Executor:
    def __init__(self):
        self.vars = VariableTable()
        self.functions = FunctionRegistry()
        self.functions.executor = self

    def execute(self, concepts):
        action = concepts["action"]
        name = concepts.get("name")
        target = self.vars.get(name) or self.vars.current

        # Functions
        if action=="define_function":
            self.functions.define(concepts["name"], concepts.get("args",[]), concepts.get("body",[]))
            return
        if action=="call_function":
            self.functions.call(concepts["name"], concepts.get("args",[]))
            return

         # ARITHMETIC (no data structure involved)
        if action=="calculate":
            numbers = concepts.get("numbers",[])
            op = concepts.get("operator","+")
            if len(numbers) < 2:
                print("Need at least two numbers to calculate")
                return
            result = numbers[0]
            for n in numbers[1:]:
                if op=="+": result += n
                elif op=="-": result -= n
                elif op=="*": result *= n
                elif op=="/": result = result/n if n else float("inf")
            print(result)
            return

        # CREATE DSA
        if action=="create":
            ds_type = concepts["type"]
            obj = DSA_TYPES[ds_type]()
            if name:
                self.vars.set(name,obj)
            else:
                self.vars.current = obj
            print(f"{ds_type} created{' as '+name if name else ''}")
            return

        # ADD / INSERT / PUSH / ENQUEUE
        if action=="add":
            if target is None:
                print("No object exists")
                return
            for v in concepts.get("numbers",[]):
                target.execute("add",v)

        # REMOVE / POP / DELETE
        if action=="remove":
            if target is None:
                print("No object exists")
                return
            target.execute("remove")

        # GRAPH EDGE
        if action in ["add_edge","add_weighted_edge"]:
            if target is None:
                print("No graph exists")
                return
            target.execute(action,concepts.get("value"))

        # PRINT
        if action=="print":
            if target is None:
                print("No object exists")
                return
            target.execute("print")

        # LOOP
        if action=="loop":
            times = concepts.get("times",1)
            body_text = concepts.get("body")
            for _ in range(times):
                if body_text:
                    body_concepts = extract_action_entities(body_text)
                    self.execute(body_concepts)

        # CONDITIONAL
        if action=="if":
            cond = concepts.get("condition")
            body_text = concepts.get("body")
            if target is None:
                target = self.vars.current
            try:
                cond_eval = eval(cond)
            except:
                cond_eval = False
            if cond_eval and body_text:
                body_concepts = extract_action_entities(body_text)
                self.execute(body_concepts)
