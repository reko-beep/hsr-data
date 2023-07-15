import json
import os
import sys
from pathlib import Path
from typing import Generator


class TracesEmbedBuff:
    def __init__(self, content: dict | None = None) -> None:
        if content is None:
            sys.exit("Missing 1 argument: json file content")
        self.content = content

    def skilltree_points(self) -> Generator[dict, None, None]:
        traces_data: list = self.content["skillTreePoints"]
        for data in traces_data:
            yield data

    def traces(self):
        for data in self.skilltree_points():
            embed_bonus_skill = data.get("embedBonusSkill")
            if embed_bonus_skill is None:
                continue
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

    def skilltreepoints_embedbuff_children0(self):
        for data in self.skilltree_points():
            embedBuff0 = data.get("embedBuff")
            if embedBuff0 is None:
                continue
            yield embedBuff0

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
