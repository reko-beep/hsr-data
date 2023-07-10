import json

class Playercards:
    def __init__(self, pcard_id: int):
        with open(f"raw_data/en/playercards/{pcard_id}") as file:
            self.content: dict = json.loads(file.read())