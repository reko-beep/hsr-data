import json
import os
import sys
from pathlib import Path
from typing import Generator


class Character:
    def __init__(self, name: str | None = None) -> None:
        if name is None:
            sys.exit("Missing 1 argument: name of character")
        os.chdir(Path(__file__).parent.parent)
        with open(f"raw_data/en/characters/{name}.json") as file:
            self.content: dict = json.loads(file.read())

    def skilltree_points(self) -> Generator[dict, None, None]:
        traces_data: list = self.content["skillTreePoints"]
        for data in traces_data:
            yield data

    def traces(self):
        for data in self.skilltree_points():
            embed_bonus_skill = data.get("embedBonusSkill")
            yield embed_bonus_skill

    def skilltreepoints_children1(self):
        for data in self.skilltree_points():
            children1 = data.get("children")
            if children1 is None:
                continue
            for children in children1:
                yield children

    def skilltreepoints_children2(self):
        for data in self.skilltreepoints_children1():
            children2 = data.get("children")
            if children2 is None:
                continue
            yield children2

    def skilltreepoints_children3(self):
        for datas in self.skilltreepoints_children2():
            for data in datas:
                children3 = data.get("children")
                if children3 is None:
                    continue
                yield children3

    def skilltreepoints_embedbuff_children1(self):
        for datas in self.skilltreepoints_children1():
            embed_buff1 = datas.get("embedBuff")
            if embed_buff1 is None:
                continue
            yield embed_buff1

    def skilltreepoints_embedbuff_children2(self):
        for datas in self.skilltreepoints_children2():
            for data in datas:
                embed_buff2 = data.get("embedBuff")
                if embed_buff2 is None:
                    continue
                yield embed_buff2

    def skilltreepoints_embedbuff_children3(self):
        for datas in self.skilltreepoints_children3():
            for data in datas:
                embed_buff3 = data.get("embedBuff")
                if embed_buff3 is None:
                    continue
                yield embed_buff3


char = Character("bailu")
for data in char.skilltreepoints_embedbuff_children3():
    print(data)
    print()
