import re

def extract_numbers(text):
    return [int(n) for n in re.findall(r'\d+', text)]

def evaluate_expression(expr):
    try:
        return eval(expr)
    except:
        return None
