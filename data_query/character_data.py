import json
import os
from collections import defaultdict
from typing import Dict, Generator, Tuple, List, Any, LiteralString


class Character:
    def __init__(self, name: str) -> None:
        self.content: Dict
        os.chdir(r"K:\GitHub_Desktop\hsr-data-bot")
        with open(f"raw_data/en/characters/{name}.json") as file:
            self.content = json.loads(file.read())

    def json_data(self) -> List[str]:
        category: str
        return [category for category in self.content]

    def name(self) -> str:
        return self.content["name"]

    def damage_type(self) -> str:
        return self.content["damageType"]["name"]

    def path(self) -> str:
        return self.content["baseType"]["name"]

    def stat_data_max(self) -> Generator[Tuple[str, float], None, None]:
        data: str
        value: float
        stat_dict = self.content["levelData"][-1]
        for data, value in stat_dict.items():
            if isinstance(value, list) and len(value) == 0:
                pass
            else:
                yield data, value

    def stat_at_max(self) -> Tuple[float, float, float, float]:
        max_stats: Dict = defaultdict(str)
        stat: str
        value: float
        for stat, value in self.stat_data_max():
            max_stats[stat] = value
        base_attack: float = max_stats["attackBase"]
        base_hp: float = max_stats["hpBase"]
        base_def: float = max_stats["defenseBase"]
        base_speed: float = max_stats["speedBase"]
        return base_attack, base_hp, base_def, base_speed

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
