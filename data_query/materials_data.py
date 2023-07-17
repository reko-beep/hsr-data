import json
import os
from pathlib import Path


class Materials:
    def __init__(self, mats_id: int | None = None):
        if mats_id is None:
            sys.exit("Missing 1 argument: id of material")
        os.chdir(Path(__file__).parent.parent)
        with open(f"raw_data/en/materials/{mats_id}.json") as file:
            self.content: dict = json.loads(file.read())

    def name(self) -> str | None:
        name = self.content.get("name")
        if name is None:
            return
        return name

    def id(self) -> str | None:
        embedded_item: dict | None = self.content.get("embeddedItem")
        if embedded_item is None:
            return
        id = embedded_item.get("id")
        if id is None:
            return
        return id

    def rarity(self) -> str | None:
        rarity = self.content.get("rarity")
        if rarity is None:
            return
        return rarity

    def drop_location(self):
        droplocation = self.content.get("comeFrom")
        return droplocation
