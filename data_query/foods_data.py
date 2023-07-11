import json


class Foods:
    def __init__(self, food_id: int):
        with open(f"raw_data/en/foods/{food_id}.json") as file:
            self.content: dict = json.loads(file.read())
