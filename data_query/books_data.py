import json
import os
import re
from unicodedata import normalize
from pathlib import Path
from collections import defaultdict
import data_query.shared_data.shared_var as SharedVar


class Books:
    def __init__(self, book_id: int):
        os.chdir(Path(__file__).parent.parent)
        with open(f"raw_data/en/books/{book_id}.json") as file:
            self.content: dict = json.loads(file.read())

    def name(self) -> str:
        name = self.content.get("name")
        return SharedVar.readable_deschash_text(name)

    def book_id(self) -> int:
        return int(self.content.get("pageId"))

    def iconPath(self) -> str:
        return self.content.get("icontPath")

    def description(self) -> str:
        return self.content.get("desc")

    def volumes(self) -> list:
        volumes: list = self.content.get("volumes")
        volumes_dict = defaultdict(str)
        volumes_list = []
        for index, volume in enumerate(volumes):
            title: str = normalize("NFKC", volume.get("title"))
            local_title: str = volume.get("localTitle")
            local_desc: str = volume.get("localDesc")
            local_desc_cleaned = SharedVar.readable_deschash_text(local_desc)
            local_desc_cleaned_normalized = normalize("NFKD", local_desc_cleaned)
            desc = re.sub(r"\\", "", local_desc_cleaned_normalized, re.IGNORECASE)
            images: list = volume.get("images")
            volumes_list.append((title, local_title, desc, images))
        return volumes_list
