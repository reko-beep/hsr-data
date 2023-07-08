import json
import sys
import re
from collections import defaultdict
from typing import Dict, Generator, Tuple, List, Any
from itertools import count
from data_query.query_errors.errors import *
from data_query.shared_data.shared_var import SharedVar


class Character:
    def __init__(self, name: str | None = None) -> None:
        if name is not None:
            with open(f"raw_data/en/characters/{name}.json") as file:
                self.content: Dict = json.loads(file.read())
        else:
            sys.exit("Missing 1 argument: name of character")

    def json_data(self) -> List[str]:
        """
        Returns a list containing available data from the character.

        json_data = Character("character_name").json_data()
        for data in json_data:
            print(data)
        """
        return [category for category in self.content]

    def name(self) -> str:
        """
        Returns character's Name.

        print(Character("character_name").name())
        """
        return self.content["name"]

    def rarity(self) -> int:
        """
        Returns character's Rarity.

        print(Character("character_name").rarity())
        """
        return self.content["rarity"]

    def damage_type(self) -> str:
        """
        Returns character's Damage Type.

        print(Character("character_name").damage_type())
        """
        return self.content["damageType"]["name"]

    def path(self) -> str:
        """
        Returns character's Path.

        print(Character("character_name").path())
        """
        return self.content["baseType"]["name"]

    def stat_data_onlevel(self, level: int = 80) -> Dict | str:
        """
        Returns character's base stat on every ascension.

        print(Character("character_name").stat_data_onlevel(80))
        """
        level_list = SharedVar.level()
        if level in level_list and isinstance(level, int):
            stat_dict: List[Dict] = self.content["levelData"]
            for data in stat_dict:
                if data["maxLevel"] == level:
                    return data
        else:
            raise LevelOutOfRangeError

    def stat_data_max(self) -> Generator[Tuple[str, float], None, None]:
        """
        Returns a generator object containing the base stat data of a
        character at max level.

        stat_data_max = Character("character_name").stat_data_max()
        for data in stat_data_max():
            print(data)
        """
        stat_dict = self.content["levelData"][-1]
        for data, value in stat_dict.items():
            if isinstance(value, list) and len(value) == 0:
                pass
            else:
                yield data, value

    def stat_at_max(self) -> dict:
        """
        Returns character's base stat at max level

        stat_data_max = Character("character_name").stat_data_max()
        for data in stat_data_max():
            print(data)
        """
        max_stats: Dict = defaultdict(float)
        for stat, value in self.stat_data_max():
            max_stats[stat] = float(value)
        return max_stats

    def get_skill_data(self) -> dict:
        """
        Returns character's Skill data

        print(Character("character_name").skills())
        """
        return self.content["skills"]

    def trace(self) -> Generator[dict, None, None]:
        """
        Returns a generator object containing character's Traces data

        trace = Character("character_name").trace())
        for data in trace:
            print(data)
        """
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
        """
        Returns a generator object containing characater's Constellation data.

        constellation = Character("character_name").constellation())
        for data in constellaton:
            print(data)
        """
        const_data: List = self.content["ranks"]
        for data in const_data:
            const_name: str = data.get("name")
            const_desc: str = data.get("descHash")
            const_params: List[float] = data.get("params")
            if len(const_params) != 0:
                yield const_name, const_desc, const_params
            else:
                yield const_name, const_desc, None

    def skill_general(self, typeDesc: str, level: int = 1) -> Dict[str, Any]:
        current_skill = self.get_typeDescHash(typeDesc)
        skill_params = self.get_skillparams_onlevel(typeDesc, level)
        atktype = current_skill["tagHash"]
        descHash = current_skill["descHash"]
        descHash_cleaned: str = re.sub("<[^\>]+.", "", descHash)
        return skill_params

    def get_skillparams_onlevel(self, typeDesc, level):
        get_skill_category = self.get_typeDescHash(typeDesc)
        levelData = get_skill_category["levelData"]
        max_level = len(levelData)
        if level > max_level:
            raise SkillLevelOutOfrange
        else:
            for params in levelData:
                if params["level"] == level:
                    return params

    def get_typeDescHash(self, get_data):
        for data in self.get_skill_data():
            if data["typeDescHash"] == get_data:
                basicatk_data: Dict = data
        return basicatk_data

    def skill_basicatk(self, level: int):
        return self.skill_general("Basic ATK", level)

    def skill_skill(self, level: int):
        return self.skill_general("Skill", level)

    def skill_ultimate(self, level: int):
        return self.skill_general("Ultimate", level)

    def skill_talent(self, level: int):
        return self.skill_general("Talent", level)

    def skill_technique(self, level: int):
        return self.skill_general("Technique", level)

char = Character("bailu")
print(char.skill_technique(1))