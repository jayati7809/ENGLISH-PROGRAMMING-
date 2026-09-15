import os
from helper import extract_numbers, evaluate_expression
from engine.llm_parser import extract_action_entities_llm

# Set EAPL_USE_LLM=0 to skip Ollama entirely and always use the rule-based
# parser below (useful if Ollama isn't installed/running on this machine).
USE_LLM = os.environ.get("EAPL_USE_LLM", "1") != "0"


def extract_action_entities(text):
    """Try the LLM (Ollama) first so synonyms like add/insert/push/plus all
    resolve correctly. If Ollama is unreachable or returns something bad,
    fall back to the rule-based parser so the tool still works offline."""
    if USE_LLM:
        try:
            return extract_action_entities_llm(text)
        except Exception as e:
            print(f"[llm_parser] falling back to rule-based parser ({e})")
    return _rule_based_extract(text)


def _rule_based_extract(text):
    text = text.lower()
    numbers = extract_numbers(text)
    words = text.split()

        # Named object
    name = None
    if "called" in words:
        idx = words.index("called")
        if idx+1 < len(words):
            name = words[idx+1]

    # Does this sentence reference an actual data structure to act on?
    has_target_phrase = (" to " in f" {text} " or " onto " in f" {text} "
                          or " into " in f" {text} " or name is not None)

    # Pure arithmetic (no target structure mentioned) -> calculate a result
    op_words = {
        "add":"+", "plus":"+", "sum":"+",
        "subtract":"-", "minus":"-",
        "multiply":"*", "times":"*",
        "divide":"/", "divided":"/",
    }
    if not has_target_phrase and len(numbers) >= 2:
        for w, op in op_words.items():
            if w in words:
                return {"action":"calculate","operator":op,"numbers":numbers}


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

    # Print / show / display
    if any(a in words for a in ["print","show","display"]):
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

