
def parse_conditional(concepts):
    """
    Convert English conditional concepts into a structured form.

    Expected English examples:
    - "if x is greater than 5 then print x"
    - "if total equals 10 then print total else print 0"
    """

    condition = concepts.get("condition")
    then_block = concepts.get("then", [])
    else_block = concepts.get("else", [])

    if condition is None:
        raise Exception("Condition is missing in 'if' statement")

    return {
        "type": "if",
        "condition": condition,     # string expression
        "then": then_block,         # list of actions
        "else": else_block          # list of actions
    }
