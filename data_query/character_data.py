import json
import os
from collections import defaultdict
from typing import Dict, Generator, Tuple, List, Any
from itertools import count
from data_query.query_errors.error_msg import QueryError

class Character:
    def __init__(self, name: str) -> None:
        with open(f"raw_data/en/characters/{name}.json") as file:
            self.content: Dict = json.loads(file.read())

    def json_data(self) -> List[str]:
        category: str
        return [category for category in self.content]

    def name(self) -> str:
        return self.content["name"]

    def damage_type(self) -> str:
        return self.content["damageType"]["name"]

    def path(self) -> str:
        return self.content["baseType"]["name"]

    def stat_data_onlevel(self, level: int) -> Dict | str:
        level_iterator = count(start = 20, step = 10)
        level_list: List = list(next(level_iterator) for _ in range(7))
        if level in level_list:
            stat_dict: Dict = self.content["levelData"]
            for data in stat_dict:
                if data["maxLevel"] == level:
                    return data
        else:
            return QueryError.leveldata_outofrange()

    def stat_data_max(self) -> Generator[Tuple[str, float], None, None]:
        stat_dict = self.content["levelData"][-1]
        for data, value in stat_dict.items():
            if isinstance(value, list) and len(value) == 0:
                pass
            else:
                yield data, value

    def stat_at_max(self) -> dict:
        max_stats: Dict = defaultdict(float)
        for stat, value in self.stat_data_max():
            max_stats[stat] = float(value)
        return max_stats

    def skills(self) -> dict:
        skills_data: List = self.content["skills"]
        skill_dict: Dict = {}
        skill_name: List = []
        for skills in skills_data:
            skill_name.append(skills["name"])
        for name in skill_name:
            for skills in skills_data:
                if skills["name"] == name:
                    skill_dict[name] = skills
        return skill_dict

    def trace(self) -> Generator[dict, None, None]:
        traces_data: List = self.content["skillTreePoints"]
        for data in traces_data:
            trace = data.get("embedBonusSkill")
            if trace is not None:
                yield trace
            else:
                pass

    def constellation(
        self,
    ) -> (
        Generator[Tuple[str, str, List[float]], None, None]
        | Generator[Tuple[str, str, None], None, None]
    ):
        const_data: List = self.content["ranks"]
        for data in const_data:
            const_name: str = data.get("name")
            const_desc: str = data.get("descHash")
            const_params: List[float] = data.get("params")
            if len(const_params) != 0:
                yield const_name, const_desc, const_params
            else:
                yield const_name, const_desc, None

