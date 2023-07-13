import json
import re
import os
from typing import Generator, Any
from data_query.shared_data.shared_var import readable_descHash


class Relic:
    def __init__(self, relic_id: int = None):
        if relic_id is None:
            sys.exit("Missing 1 argument: id of relic")
        with open(f"raw_data/en/relics/{relic_id}.json") as file:
            self.content: dict = json.loads(file.read())

    def name(self) -> str | None:
        data = self.content.get("name")
        if data is None:
            return
        return data

    def id(self) -> int | None:
        id: str | None = self.content.get("pageId")
        if id is None:
            return
        return int(id)

    def rarity(self) -> int | None:
        rarity = self.content.get("rarity")
        if rarity is None:
            return
        return int(rarity)

    def set_bonus(self) -> Generator[tuple[int, str] | None, None, None]:
        skill_data: list[dict] | None = self.content.get("skills")
        if skill_data is None:
            return
        for data in skill_data:
            desc: str = data.get("desc")
            params: list[float] = data.get("params")
            set_num: int = data.get("useNum")
            output: str = "relic"
            name: str | None = self.name()
            if desc and params and set_num and name is None:
                return
            yield (
                set_num,
                readable_descHash(name, params, desc, set_num, output),
            )

    def pieces_effect_data(self) -> list[dict] | None:
        pieces_data: dict | None = self.content.get("pieces")
        if pieces_data is None:
            return
        set_piece_num = pieces_data.keys()
        pieces_effect_list = []
        for num in set_piece_num:
            set_piece: dict | None = pieces_data.get(num)  # inside "pieces" now
            if set_piece is None:
                return
            piece_name: str = set_piece.get("name")
            max_rarity: int = set_piece.get("maxRarity")
            piece_part: str = set_piece.get("baseTypeText")
            rarity_data: dict = set_piece.get("rarityData")
            pieces_effect_list.append(
                {
                    "name": piece_name,
                    "maxRarity": max_rarity,
                    "baseTypeText": piece_part,
                    "rarityData": rarity_data,
                }
            )
        return pieces_effect_list

    def main_stat(self, stat: str = "main") -> Generator[dict, None, None]:
        pieces_data: list[dict] | None = self.pieces_effect_data()
        if pieces_data is None:
            return
        for data in pieces_data:
            name: str = data.get("name")
            piece_part: str = data.get("baseTypeText")
            rarity_data: dict | None = data.get("rarityData")
            if rarity_data is None:
                return
            for key in rarity_data.keys():
                stat_raw: dict = rarity_data[key]
                propertyicon_path: str = stat_raw.get("propertyIconPath")
                max_level: int = stat_raw.get("maxLevel")
                main_stat: list = stat_raw.get("mainAffixes")
                yield {
                    "rarity": int(key),
                    "name": name,
                    "baseTypeText": piece_part,
                    "maxLevel": max_level,
                    "mainAffixes": main_stat,
                }

    def sub_stat(self) -> Generator[dict, None, None] | None:
        pieces_data: list[dict] | None = self.pieces_effect_data()
        if pieces_data is None:
            return
        for data in pieces_data:
            name: str = data.get("name")
            piece_part: str = data.get("baseTypeText")
            rarity_data: dict | None = data.get("rarityData")
            if rarity_data is None:
                return
            for key in rarity_data.keys():
                stat_raw: dict = rarity_data[key]
                sub_stats: list | None = stat_raw.get("subAffixes")
                if sub_stats is None:
                    return
                for sub_stat in sub_stats:
                    sub_stat_name: str = sub_stat.get("propertyName")
                    sub_stat_propertyicon: str = sub_stat.get("propertyIconPath")
                    sub_stat_ispercent: bool = sub_stat.get("isPercent")
                    base_value: float | int = sub_stat.get("baseValue")
                    level_add: float | int = sub_stat.get("levelAdd")
                    step_value: float | int = sub_stat.get("stepValue")
                    max_step: int = sub_stat.get("maxStep")
                    yield {
                        "name": name,
                        "isPercent": sub_stat_ispercent,
                        "baseTypeText": piece_part,
                        "rarity": int(key),
                        "propertyName": sub_stat_name,
                        "propertyIconPath": sub_stat_propertyicon,
                        "baseValue": base_value,
                        "levelAdd": level_add,
                        "stepValue": step_value,
                    }
