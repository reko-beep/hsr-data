import json
import re
import os
from typing import Generator, Any
from data_query.shared_data.shared_var import readable_descHash


class Relic:
    def __init__(self, relic_id: int):
        with open(f"raw_data/en/relics/{relic_id}.json") as file:
            self.content: dict = json.loads(file.read())

    def name(self) -> str:
        data = self.content.get("name")
        if data is not None:
            return data

    def set_bonus(self) -> Generator[str, None, None]:
        skill_data: list[dict] | None = self.content.get("skills")
        if skill_data is not None:
            for data in skill_data:
                desc: str | None = data.get("desc")
                params: list[float] | None = data.get("params")
                set_num: int | None = data.get("useNum")
                output = "relic"
                if desc and params and set_num is not None:
                    yield readable_descHash(self.name(), params, desc, set_num, output)

    def pieces_effect_data(self) -> list[dict]:
        pieces_data: dict | None = self.content.get("pieces")
        if pieces_data is not None:
            set_piece_num = pieces_data.keys()
            pieces_effect_list = []
            for num in set_piece_num:
                set_piece = pieces_data.get(num)  # inside "pieces" now
                piece_name: str = set_piece.get("name")
                max_rarity: int = set_piece.get("maxRarity")
                piece_part: str = set_piece.get("baseTypeText")
                rarity_data: dict[str[dict]] = set_piece.get("rarityData")
                pieces_effect_list.append(
                    {
                        "name": piece_name,
                        "maxRarity": max_rarity,
                        "baseTypeText": piece_part,
                        "rarityData": rarity_data,
                    }
                )
            return pieces_effect_list

    def piece_main_stat(self) -> Generator[[dict[str, Any]], None, None]:
        pieces_data: list[dict] = self.pieces_effect_data()
        for data in pieces_data:
            name = data.get("name")
            piece_part = data.get("baseTypeText")
            rarity_data = data.get("rarityData")
            for key in rarity_data.keys():
                main_stat_raw: dict = rarity_data[key]
                main_stat: list = main_stat_raw.get("mainAffixes")
                yield {
                    "rarity": key,
                    "name": name,
                    "baseTypeText": piece_part,
                    "mainAffixes": main_stat,
                }


if __name__ == "__main__":
    # for filename in os.listdir("raw_data/en/relics"):
    #     if ".json" in filename:
    #         id = filename.replace(".json", "")
    #         relic = Relic(id)
    #         for data in relic.set_bonus():
    #             print(data)
    relic = Relic(101)
    # print(relic.pieces_effect_data())
    for data in relic.piece_main_stat():
        if data.get("baseTypeText") == "Hands":
            print(data)
