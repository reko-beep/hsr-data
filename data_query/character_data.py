import json
import sys
import re
import os
import sqlite3
from dotenv import dotenv_values
from pathlib import Path
from collections import defaultdict
from typing import Generator, Any
from itertools import count
from data_query.query_errors.errors import *
import data_query.character_module.trace_module as TraceModule
import data_query.shared_data.shared_var as SharedVar
import data_query.character_module.skill_description as skill_desc


class Character:
    def __init__(self, name: str | None = None) -> None:
        if name is None:
            sys.exit("Missing 1 argument: name of character")
        os.chdir(Path(__file__).parent.parent)
        with open(f"raw_data/en/characters/{name}.json") as file:
            self.content: dict = json.loads(file.read())

    def json_data(self) -> list[str]:
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

    def stat_data_onlevel(self, level: int = 80) -> dict | str:  # type: ignore
        """
        Returns character's base stat on every ascension.

        print(Character("character_name").stat_data_onlevel(80))
        """
        level_list = SharedVar.level()
        if level not in level_list or isinstance(level, int) == False:
            raise LevelOutOfRangeError
        stat_dict: list[dict] = self.content["levelData"]
        for data in stat_dict:
            if data["maxLevel"] == level:
                return data

    def trace(self) -> dict:
        """
        Returns a dictionary containing character's Traces data

        trace = Character("character_name").trace())
        print(trace)
        """
        named_traceslist = TraceModule.trace_namedskills(self.content)
        trace_data = TraceModule.trace_embedbuffs(named_traceslist)
        unnamed_buff = TraceModule.skilltreepoints_embedbuff_children0(self.content)
        list_unnamedbuff = [buff for buff in unnamed_buff]
        trace_data["UnnamedBuff"] = list_unnamedbuff
        return trace_data

    def constellation(
        self,
    ) -> Generator[str, None, None]:
        """
        Returns a generator object containing characater's Constellation data.

        constellation = Character("character_name").constellation())
        for data in constellaton:
            print(data)
        """
        const_data: list = self.content["ranks"]
        for data in const_data:
            const_name: str = data.get("name")
            const_desc: str = data.get("descHash")
            const_params: list[float] = data.get("params")
            output: str = "constellation"
            descHash: str | None = SharedVar.readable_descHash(
                const_name, const_params, const_desc, "Max", output
            )
            if descHash is None:
                return
            yield SharedVar.correct_punctuations_lv(descHash)

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
