import json
import os
from pathlib import Path


class Foods:
    def __init__(self, food_id: int):
        os.chdir(Path(__file__).parent.parent)
        with open(f"raw_data/en/foods/{food_id}.json") as file:
            self.content: dict = json.loads(file.read())
