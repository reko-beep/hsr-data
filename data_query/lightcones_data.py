import json
import re
from itertools import count
from typing import Dict, List, Any, Iterator, Tuple
import data_query.shared_data.shared_var as SharedVar
from data_query.query_errors.errors import *


class LightCone:
    def __init__(self, name: int | None = None) -> None:
        with open(f"raw_data/en/lightcones/{name}.json") as file:
            self.content: Dict = json.loads(file.read())

    def json_data(self) -> List[str]:
        return [data for data in self.content.keys()]

    def name(self) -> str:
        return self.content["name"]

    def rarity(self) -> int:
        return self.content["rarity"]

    def level_data(self) -> List[Dict]:
        return self.content["levelData"]

    def level_data_onlevel(self, level: int = 80) -> Dict:
        level_list: List[int] = SharedVar.level()
        levelData: List[Dict] = self.level_data()
        if level in level_list:
            for data in levelData:
                if data["maxLevel"] == level:
                    return data
        else:
            raise LevelOutOfRangeError

    def skill_data(self) -> Dict:
        skills_data: Dict = self.content["skill"]
        return skills_data

    def skill_data_onlevel(self, level: int = 5) -> Dict:
        level_iterator: Iterator = count(start=1, step=1)
        level_list: List[int] = list(next(level_iterator) for _ in range(5))
        if level in level_list and isinstance(level, int):
            levelData: List[Dict] = self.skill_data()["levelData"]
            for data in levelData:
                if data["level"] == level:
                    return data
        else:
            raise LightConeSkillLevelOutOfRange

    def skill_descHash(self, level: int = 5) -> str:
        skill_onlevel_data: Dict | str = self.skill_data_onlevel(level)
        if isinstance(skill_onlevel_data, str):
            return skill_onlevel_data
        descHash: str = self.skill_data()["descHash"]
        name: str = self.skill_data()["name"]
        skill_params: List = skill_onlevel_data["params"]
        descHash_cleaned: str = re.sub("<[^\>]+.", "", descHash)
        return SharedVar.skill_description(name, skill_params, descHash_cleaned, level)


lc = LightCone(20000)
print(lc.skill_descHash())
