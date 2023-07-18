import json
import os
from pathlib import Path
import data_query.shared_data.shared_var as SharedVar
from unicodedata import normalize


class Playercards:
    def __init__(self, pcard_id: int):
        os.chdir(Path(__file__).parent.parent)
        with open(f"raw_data/en/playercards/{pcard_id}.json") as file:
            self.content: dict = json.loads(file.read())

    def name(self) -> str:
        return normalize("NFKD", self.content.get("name"))

    def rarity(self) -> int:
        return self.content.get("rarity")

    def pcard_id(self) -> int:
        return int(self.content.get("pageId"))

    def icon_path(self) -> str:
        return self.content.get("iconPath")

    def description(self):
        embedded_item: dict = self.content.get("embeddedItem")
        desc = embedded_item.get("desc")
        type = embedded_item.get("type")
        lore = embedded_item.get("lore")
        lore_cleaned = SharedVar.readable_deschash_text(lore)
        return {"desc": desc, "type": type, "lore": lore_cleaned}