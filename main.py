from engine.executor import Executor

print("=== EAPL: Syntax-Free English DSA + Functions ===")
print("Type 'exit' to quit.\n")

executor = Executor()

while True:
    text = input(">> ").strip()
    if text.lower() == "exit":
        break
    try:
        from engine.nlp_parser import extract_action_entities
        concepts = extract_action_entities(text)
        executor.execute(concepts)
    except Exception as e:
        print("Error:", e)
