"""
LLM-backed command understanding, using a local Ollama server.

This is meant to sit IN FRONT of the rule-based parser in nlp_parser.py.
Its whole job: take whatever a developer typed ("push 5 onto it",
"insert 5", "plus 5", "enqueue 5"...) and normalize it into the exact
same concepts dict shape the executor already understands, e.g.:

    {"action": "add", "numbers": [5], "name": None}

If Ollama is not running, unreachable, or returns something that
doesn't parse as valid JSON, this raises an exception on purpose —
the caller (nlp_parser.extract_action_entities) is responsible for
catching that and falling back to the rule-based parser.
"""

import json
import os
import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")
OLLAMA_TIMEOUT = float(os.environ.get("OLLAMA_TIMEOUT", "60"))

SYSTEM_PROMPT = """You are a strict command parser for a tiny English-to-code interpreter.
Given one line of natural English typed by a developer, output ONE JSON object
describing what they want to do. Many different words mean the same action —
normalize them. Examples of synonyms you must treat as identical:
  add = insert = push = plus = enqueue = append
  remove = pop = dequeue = delete
  print = show = display

Allowed "action" values and their required fields:
- "calculate":   {"action":"calculate","operator":"<+|-|*|/>","numbers":[<ints>]}  — use this when the sentence is pure arithmetic with NO data structure or "to/onto/into <name>" mentioned, e.g. "add 5 and 10", "multiply 3 and 4".
- "create":      {"action":"create","type":"<stack|queue|list|array|linkedlist|bst|heap|graph>","name":<string or null>}
- "add":         {"action":"add","numbers":[<ints>],"name":<string or null>}  — use this ONLY when the sentence mentions adding INTO/ONTO/TO a data structure (by name, or an already-created one), e.g. "add 5 and 10 to mylist", "push 3 onto it".
- "remove":      {"action":"remove","numbers":[<ints>],"name":<string or null>}
- "add_edge":    {"action":"add_edge","value":[<u>,<v>],"name":<string or null>}
- "add_weighted_edge": {"action":"add_weighted_edge","value":[<u>,<v>,<w>],"name":<string or null>}
- "print":       {"action":"print","name":<string or null>}
- "loop":        {"action":"loop","times":<int>,"body":"<remaining instruction text>","name":<string or null>}
- "if":          {"action":"if","condition":"<python-evaluable condition text>","body":"<remaining instruction text>","name":<string or null>}
- "define_function": {"action":"define_function","name":"<fn name>","args":["<arg names>"],"body":["<statement>", ...]}
- "call_function":   {"action":"call_function","name":"<fn name>","args":[<ints>]}

Rules:
- Output ONLY the JSON object. No prose, no markdown fences, no explanation.
- "name" is the identifier after the word "called", if present, else null.
- If you truly cannot classify the line, output {"action":"unknown","raw":"<the line>"}.
"""

FEW_SHOT = [
    ("add 5 and 10", {"action": "calculate", "operator": "+", "numbers": [5, 10]}),
    ("multiply 3 and 4", {"action": "calculate", "operator": "*", "numbers": [3, 4]}),
    ("create a stack called mystack", {"action": "create", "type": "stack", "name": "mystack"}),
    ("push 5 onto it", {"action": "add", "numbers": [5], "name": None}),
    ("add 7 and 8 to mystack", {"action": "add", "numbers": [7, 8], "name": "mystack"}),
    ("pop from mystack", {"action": "remove", "numbers": [], "name": "mystack"}),
    ("show mystack", {"action": "print", "name": "mystack"}),
]


def _build_prompt(text):
    examples = "\n".join(
        f'Developer said: "{u}"\nJSON: {json.dumps(j)}' for u, j in FEW_SHOT
    )
    return f"{SYSTEM_PROMPT}\n{examples}\n\nDeveloper said: \"{text}\"\nJSON:"


def _clean_json(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
    return raw.strip()


def ask_ollama(text):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": _build_prompt(text),
        "stream": False,
        "format": "json",
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    raw = data.get("response", "")
    cleaned = _clean_json(raw)
    return json.loads(cleaned)


def extract_action_entities_llm(text):
    parsed = ask_ollama(text)
    if not isinstance(parsed, dict) or "action" not in parsed:
        raise ValueError(f"LLM returned an unusable response: {parsed!r}")
    if parsed["action"] == "unknown":
        raise ValueError(f"LLM could not classify: {text!r}")
    return parsed