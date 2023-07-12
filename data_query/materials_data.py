import json


class Materials:
    def __init__(self, mats_id: int):
        with open(f"raw_data/en/materials/{mats_id}.json") as file:
            self.content: dict = json.loads(file.read())

    def name(self) -> str | None:
        name = self.content.get("name")
        if name is not None:
            return name
        else:
            return None

    def id(self) -> str | None:
        embedded_item: dict | None = self.content.get("embeddedItem")
        if embedded_item is not None:
            id = embedded_item.get("id")
            if id is not None:
                return id
            else:
                return None
        else:
            return None

    def rarity(self) -> str | None:
        rarity = self.content.get("rarity")
        if rarity is not None:
            return rarity
        else:
            return None
