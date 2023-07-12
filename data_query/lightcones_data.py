import json
import re
from itertools import count
from typing import Any, Iterator
import data_query.shared_data.shared_var as SharedVar
from data_query.query_errors.errors import *


class LightCone:
    def __init__(self, name: int | None = None) -> None:
        with open(f"raw_data/en/lightcones/{name}.json") as file:
            self.content: dict = json.loads(file.read())

    def json_data(self) -> list[str]:
        return [data for data in self.content.keys()]

    def name(self) -> str:
        return self.content["name"]

    def lc_id(self) -> int:
        return int(self.content["pageId"])

    def rarity(self) -> int:
        return self.content["rarity"]

    def level_data_onlevel(self, level: int = 80) -> dict | None:  # type: ignore
        level_data = self.content["levelData"]
        level_list: list[int] = SharedVar.level()
        levelData: list[dict] = level_data
        if level in level_list:
            for data in levelData:
                if data["maxLevel"] == level:
                    return data
        else:
            raise LevelOutOfRangeError

    def skill_data(self) -> dict:
        skills_data: dict = self.content["skill"]
        return skills_data

    def skill_data_onlevel(self, level: int = 5) -> dict | None:  # type: ignore
        level_iterator: Iterator = count(start=1, step=1)
        level_list: list[int] = list(next(level_iterator) for _ in range(5))
        if level in level_list and isinstance(level, int):
            levelData: list[dict] = self.skill_data()["levelData"]
            for data in levelData:
                if data["level"] == level:
                    return data
        else:
            raise LightConeSkillLevelOutOfRange

    def skill_descHash(self, level: int = 5) -> str | None:
        skill_onlevel_data: dict | None = self.skill_data_onlevel(level)
        if isinstance(skill_onlevel_data, str):
            return skill_onlevel_data
        else:
            if skill_onlevel_data is not None:
                descHash: str = self.skill_data()["descHash"]
                name: str = self.skill_data()["name"]
                skill_params: list = skill_onlevel_data["params"]
                output = "lightcone"
                return SharedVar.readable_descHash(
                    name, skill_params, descHash, level, output
                )
            else:
                return None
