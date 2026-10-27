import json

def save_json(input: str) -> None:
    with open("output.json", "w", encoding="utf-8") as file:
        file.write(input)