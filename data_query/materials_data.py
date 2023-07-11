import json


class Materials:
    def __init__(self, mats_id: int):
        with open(f"raw_data/en/materials/{mats_id}.json") as file:
            self.content: dict = json.loads(file.read())

    def name(self) -> str:
        return self.content.get("name")

    def id(self) -> str:
        embedded_item = self.content.get("embeddedItem")
        return embedded_item.get("id")

    def rarity(self) -> str:
        return self.content.get("rarity")
