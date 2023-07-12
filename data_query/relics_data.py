import json
import re
import os
from typing import Generator, Any
from data_query.shared_data.shared_var import readable_descHash


class Relic:
    def __init__(self, relic_id: int):
        with open(f"raw_data/en/relics/{relic_id}.json") as file:
            self.content: dict = json.loads(file.read())

    def name(self) -> str | None:
        data = self.content.get("name")
        if data is not None:
            return data
        else:
            return None

    def id(self) -> int | None:
        id: str | None = self.content.get("pageId")
        if id is not None:
            return int(id)
        else:
            return None

    def set_bonus(self) -> Generator[str | None, None, None]:
        skill_data: list[dict] | None = self.content.get("skills")
        if skill_data is not None:
            for data in skill_data:
                desc: str | None = data.get("desc")
                params: list[float] | None = data.get("params")
                set_num: int | None = data.get("useNum")
                output: str = "relic"
                name: str | None = self.name()
                if desc and params and set_num and name is not None:
                    yield readable_descHash(name, params, desc, set_num, output)

    def pieces_effect_data(self) -> list[dict] | None:
        pieces_data: dict | None = self.content.get("pieces")
        if pieces_data is not None:
            set_piece_num = pieces_data.keys()
            pieces_effect_list = []
            for num in set_piece_num:
                set_piece: dict | None = pieces_data.get(num)  # inside "pieces" now
                if set_piece is not None:
                    piece_name: str | None = set_piece.get("name")
                    max_rarity: int | None = set_piece.get("maxRarity")
                    piece_part: str | None = set_piece.get("baseTypeText")
                    rarity_data: dict | None = set_piece.get("rarityData")
                    pieces_effect_list.append(
                        {
                            "name": piece_name,
                            "maxRarity": max_rarity,
                            "baseTypeText": piece_part,
                            "rarityData": rarity_data,
                        }
                    )
                return pieces_effect_list
            else:
                return None
        else:
            return None

    def main_stat(self, stat: str = "main") -> Generator[dict, None, None]:
        pieces_data: list[dict] | None = self.pieces_effect_data()
        if pieces_data is not None:
            for data in pieces_data:
                name: str | None = data.get("name")
                piece_part: str | None = data.get("baseTypeText")
                rarity_data: dict | None = data.get("rarityData")
                if rarity_data is not None:
                    for key in rarity_data.keys():
                        stat_raw: dict = rarity_data[key]
                        propertyicon_path: str | None = stat_raw.get("propertyIconPath")
                        max_level: int | None = stat_raw.get("maxLevel")
                        main_stat: list | None = stat_raw.get("mainAffixes")
                        yield {
                            "rarity": int(key),
                            "name": name,
                            "baseTypeText": piece_part,
                            "maxLevel": max_level,
                            "mainAffixes": main_stat,
                        }

    def sub_stat(self) -> Generator[dict, None, None]:
        pieces_data: list[dict] | None = self.pieces_effect_data()
        if pieces_data is not None:
            for data in pieces_data:
                name: str | None = data.get("name")
                piece_part: str | None = data.get("baseTypeText")
                rarity_data: dict | None = data.get("rarityData")
                if rarity_data is not None:
                    for key in rarity_data.keys():
                        stat_raw: dict = rarity_data[key]
                        sub_stats: list | None = stat_raw.get("subAffixes")
                        if sub_stats is not None:
                            for sub_stat in sub_stats:
                                sub_stat_name: str | None = sub_stat.get("propertyName")
                                sub_stat_propertyicon: str | None = sub_stat.get(
                                    "propertyIconPath"
                                )
                                sub_stat_ispercent: bool | None = sub_stat.get(
                                    "isPercent"
                                )
                                base_value: float | int | None = sub_stat.get(
                                    "baseValue"
                                )
                                level_add: float | int | None = sub_stat.get("levelAdd")
                                step_value: float | int | None = sub_stat.get(
                                    "stepValue"
                                )
                                max_step: int | None = sub_stat.get("maxStep")
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
