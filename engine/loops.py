
def parse_loop(concepts):
    """
    Convert English loop concepts into a structured loop plan.

    Supported English examples:
    - "repeat 5 times print x"
    - "loop 10 times add 1 to x"
    - "do this 3 times"

    Expected concepts format:
    {
        "action": "loop",
        "numbers": [N],
        "body": [ ... execution steps ... ]
    }
    """

    numbers = concepts.get("numbers", [])

    if not numbers:
        raise Exception("Loop count not specified")

    times = numbers[0]

    if times <= 0:
        raise Exception("Loop count must be greater than zero")

    body = concepts.get("body", [])

    if not body:
        raise Exception("Loop body is empty")

    return {
        "type": "loop",
        "times": times,    # how many times to repeat
        "body": body      # list of planned steps
    }
