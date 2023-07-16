import json
import sys
import re
import os
import sqlite3
from dotenv import dotenv_values
from pathlib import Path
from collections import defaultdict
from typing import Dict, Generator, Tuple, List, Any
from itertools import count
from data_query.query_errors.errors import *
from data_query.character_module.traces_embed_buff import TracesEmbedBuff
import data_query.shared_data.shared_var as SharedVar
import data_query.character_module.skill_description as skill_desc


class Character:
    def __init__(self, name: str | None = None) -> None:
        if name is None:
            sys.exit("Missing 1 argument: name of character")
        os.chdir(Path(__file__).parent.parent)
        with open(f"raw_data/en/characters/{name}.json") as file:
            self.content: Dict = json.loads(file.read())

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
        if level not in level_list or isinstance(level, int) == False:
            raise LevelOutOfRangeError
        stat_dict: List[Dict] = self.content["levelData"]
        for data in stat_dict:
            if data["maxLevel"] == level:
                return data

    def trace(self) -> dict:
        """
        Returns a generator object containing character's Traces data

        trace = Character("character_name").trace())
        for data in trace:
            print(data)
        """
        traces_data: List = self.content.get("skillTreePoints")
        embed_buffs = TracesEmbedBuff(self.content)
        named_traceslist = []
        embedskill_buffs = defaultdict(list)
        for index, data in enumerate(traces_data):
            trace_skill = data.get("embedBonusSkill")
            children1 = data.get("children")
            if trace_skill is None:
                continue
            name = trace_skill.get("name")
            deschash = trace_skill.get("descHash")
            level_data = trace_skill.get("levelData")
            for data in level_data:
                level = data.get("level")
                params = data.get("params")
            output = "trace"
            readable_deschash = SharedVar.readable_descHash(
                name, params, deschash, level, output
            )
            named_traceslist.append((readable_deschash, children1))
        for data in named_traceslist:
            name: str = data[0]
            infos: list = data[1]  # list with length 1 :)
            for info in infos:
                childrens: dict = info
                embed_buff0 = childrens.get("embedBuff")
                embedskill_buffs[name] += [embed_buff0]
                children1 = childrens.get("children")
                for data1 in children1:
                    embed_buff1 = data1.get("embedBuff")
                    embedskill_buffs[name] += [embed_buff1]
                    children2 = data1.get("children")
                    if len(children2) == 0:
                        embed_buff2 = None
                    for data2 in children2:
                        embed_buff2 = data2.get("embedBuff")
                        embedskill_buffs[name] += [embed_buff2]
        return embedskill_buffs

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
            if descHash is None:
                return
            yield re.sub(r"[\.!%,:;?](?!$| )", r"\g<0> ", descHash)

    def skill_basicatk(self, level: int = 9) -> str | None:
        skill_basicatk: str | None = skill_desc.skill_general(
            "Basic ATK", level, self.content["skills"]
        )
        if skill_basicatk is None:
            return
        return skill_basicatk

    def skill_skill(self, level: int = 15) -> str | None:
        skill_skill: str | None = skill_desc.skill_general(
            "Skill", level, self.content["skills"]
        )
        if skill_skill is None:
            return
        return skill_skill

    def skill_ultimate(self, level: int = 15) -> str | None:
        skill_ultimate: str | None = skill_desc.skill_general(
            "Ultimate", level, self.content["skills"]
        )
        if skill_ultimate is None:
            return
        return skill_ultimate

    def skill_talent(self, level: int = 15) -> str | None:
        skill_talent: str | None = skill_desc.skill_general(
            "Talent", level, self.content["skills"]
        )
        if skill_talent is None:
            return
        return skill_talent

    def skill_technique(self, level: int = 1) -> str | None:
        skill_technique: str | None = skill_desc.skill_general(
            "Technique", level, self.content["skills"]
        )
        if skill_technique is None:
            return
        return skill_technique
