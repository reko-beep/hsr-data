import json
import sys
import re
from collections import defaultdict
from typing import Dict, Generator, Tuple, List, Any
from itertools import count
from data_query.query_errors.errors import *
import data_query.shared_data.shared_var as SharedVar
import data_query.character_skill.skill_description as skill_desc


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

    def stat_data_onlevel(self, level: int = 80) -> Dict | str:  # type: ignore
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

    # TODO: trace -> return a cleaned up descHash
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
    ) -> Generator[str, None, None]:
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
            output: str = "constellation"
            descHash: str | None = SharedVar.readable_descHash(
                const_name, const_params, const_desc, "Max", output
            )
            if descHash is not None:
                yield re.sub(r"[\.!%,:;?](?!$| )", r"\g<0> ", descHash)

    def skill_basicatk(self, level: int = 9) -> str | None:
        skill_basicatk: str | None = skill_desc.skill_general(
            "Basic ATK", level, self.content["skills"]
        )
        if skill_basicatk is not None:
            return skill_basicatk
        else:
            return None

    def skill_skill(self, level: int = 15) -> str | None:
        skill_skill: str | None = skill_desc.skill_general(
            "Skill", level, self.content["skills"]
        )
        if skill_skill is not None:
            return skill_skill
        else:
            return None

    def skill_ultimate(self, level: int = 15) -> str | None:
        skill_ultimate: str | None = skill_desc.skill_general(
            "Ultimate", level, self.content["skills"]
        )
        if skill_ultimate is not None:
            return skill_ultimate
        else:
            return None

    def skill_talent(self, level: int = 15) -> str | None:
        skill_talent: str | None = skill_desc.skill_general(
            "Talent", level, self.content["skills"]
        )
        if skill_talent is not None:
            return skill_talent
        else:
            return None

    def skill_technique(self, level: int = 1) -> str | None:
        skill_techinique: str | None = skill_desc.skill_general(
            "Technique", level, self.content["skills"]
        )
        if skill_techinique is not None:
            return skill_techinique
        else:
            return None
