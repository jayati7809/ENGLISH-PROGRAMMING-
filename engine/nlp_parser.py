from helper import extract_numbers, evaluate_expression

def extract_action_entities(text):
    text = text.lower()
    numbers = extract_numbers(text)
    words = text.split()

    # Named object
    name = None
    if "called" in words:
        idx = words.index("called")
        if idx+1 < len(words):
            name = words[idx+1]

    # Create DSA
    for ds in ["stack","queue","list","array","linkedlist","bst","heap","graph"]:
        if f"create {ds}" in text:
            return {"action":"create","type":ds,"name":name}

    # Arithmetic add/push/insert
    if any(a in words for a in ["add","push","insert","enqueue"]):
        value = numbers if numbers else []
        return {"action":"add","numbers":value,"name":name}

    # Remove/pop/dequeue
    if any(a in words for a in ["remove","pop","dequeue","delete"]):
        return {"action":"remove","numbers":numbers,"name":name}

    # Graph edges
    if "connect" in words or "edge" in words:
        nums = numbers
        if "weight" in words or "with weight" in text:
            w = numbers[-1]
            u,v = numbers[:-1]
            return {"action":"add_weighted_edge","value":(u,v,w),"name":name}
        elif len(nums)==2:
            return {"action":"add_edge","value":(nums[0],nums[1]),"name":name}

    # Print
    if "print" in words:
        return {"action":"print","name":name}

    # Loop
    if "repeat" in words and "times" in words:
        times = numbers[0] if numbers else 1
        body_text = text.split("then")[-1].strip() if "then" in text else ""
        return {"action":"loop","times":times,"body":body_text,"name":name}

    # Conditional
    if "if" in words:
        cond_text = text.split("then")[0].replace("if","").strip()
        body_text = text.split("then")[-1].strip() if "then" in text else ""
        return {"action":"if","condition":cond_text,"body":body_text,"name":name}

    # Functions
    if "define function" in text:
        name = text.split("define function")[1].split("with args")[0].strip()
        args_part = text.split("with args")[-1].split("do")[0].strip()
        args = [a.strip() for a in args_part.split(",")] if args_part else []
        body_lines = text.split("do")[-1].strip().split(";")
        return {"action":"define_function","name":name,"args":args,"body":body_lines}

    if "call function" in text:
        parts = text.split("call function")[1].strip().split("with")
        name = parts[0].strip()
        args = [int(a) for a in parts[1].replace("args","").split(",")] if len(parts)>1 else []
        return {"action":"call_function","name":name,"args":args}

    raise Exception(f"Cannot understand: '{text}'")

