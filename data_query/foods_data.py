import json
import os
from pathlib import Path
import data_query.shared_data.shared_var as SharedVar


class Foods:
    def __init__(self, food_id: int):
        os.chdir(Path(__file__).parent.parent)
        with open(f"raw_data/en/foods/{food_id}.json") as file:
            self.content: dict = json.loads(file.read())

    def name(self) -> str:
        return self.content.get("name")

    def food_id(self) -> int:
        return int(self.content.get("pageId"))

    def rarity(self) -> int:
        return self.content.get("rarity")

    def description(self) -> str:
        embedded_item: dict = self.content.get("embeddedItem")
        food_desc: str = embedded_item.get("desc")
        food_desc_cleaned = SharedVar.readable_deschash_text(food_desc)
        return food_desc_cleaned

    def food_type(self) -> str:
        compose_data: list = self.content.get("composeData")
        for data in compose_data:
            tag = data.get("tag")
            food_type = tag.get("name")
            return food_type

    def drop_location(self) -> list:
        embedded_item: dict = self.content.get("embeddedItem")
        come_from: list = embedded_item.get("comeFrom")
        return come_from


print(Foods(991869).drop_location())
