import json

def save_json(input: dict) -> None:
    with open("output.json", "w", encoding="utf-8") as file:
        json.dump(input, file, indent=2)