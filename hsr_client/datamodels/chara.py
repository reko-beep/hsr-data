
from typing import Dict, List
from bs4 import BeautifulSoup
from pydantic import BaseModel, PrivateAttr
from hsr_client.datamodels.trace import Skill



from hsr_client.datamodels.eidolon import Eidolon
from hsr_client.datamodels.element import Element
from hsr_client.datamodels.lightcone import MaterialCount
from hsr_client.hsr_types import Level
from . import trace
from hsr_client.paths import Path

from enum import Enum


class Stats(BaseModel):
    ATK: float
    HP: float
    DEF: float
    CRIT: float
    CDMG: float
    SPD: float
    TAUNT: float


# TODO: decide all the parameters
class Character(BaseModel):
    """Traces possessed by the `Character`"""
    name: str
    """Name of the Character"""
    rarity: int
    """Rarity of the Character"""
    element: Element
    """Element of the Character"""
    description: str
    """short description about the character."""
    path: Path
    """Path followed by the Character`"""
    eidolons: List[Eidolon]
    """Character's Eidolons"""
    traces: list[trace.Trace]
    """Character's Traces, does not include Skills, use `skills()` instead."""

    # srs backend levelData contains stats and ascension mats data.
    _chara_levelData = PrivateAttr()
    # srs backend skills; contains skill data and its ascension data
    _chara_skills = PrivateAttr()
    _backend = PrivateAttr()

    def stats(self, level, ascended=False) -> Stats:
        """
        Get Character's Stats for the given level. when `ascended=True` is used
        on levels where ascension is possible, gives `Stats` for ascended levels
        instead.
        """
        if level < 1 or level > 80: # TODO: or is this 90?
            raise ValueError(" 1 <= level <= 80 criteria not satisfied.")
        
        for ascension_entry in self._chara_levelData:
            if level <= ascension_entry["maxLevel"]:
                if ascension_entry["maxLevel"] == level and ascended == True:
                    continue
                
                return Stats(
                    ATK=ascension_entry["attackBase"] + ascension_entry["attackAdd"] * (level - 1),
                    HP=ascension_entry["hpBase"] + ascension_entry["hpAdd"] * (level - 1),
                    DEF=ascension_entry["defenseBase"] + ascension_entry["defenseAdd"] * (level - 1),
                    SPD=ascension_entry["speedBase"] + ascension_entry["speedAdd"] * (level - 1),
                    CRIT=ascension_entry["crate"] * 100,
                    CDMG=ascension_entry["cdmg"] * 100,
                    TAUNT=ascension_entry["aggro"],
                )

    def ascension_mats(self) -> Dict[Level, List[MaterialCount]]:
        """
        Returns the ascension materails grouped by ascension level.
        
        ```
        # example
        mats_to_ascend_beyond_level_20 = chara.ascension_mats[20]
        
        for ascension_mat in mats_to_ascend_beyond_level_20:
            print(ascension_mat.material.name)
            print(ascension_mat.material.description)
            print(ascension_mat.count)
        ```

        """
        ascension_mats = {}
        for per_ascension_data in self._chara_levelData:
            
            level = per_ascension_data['maxLevel']
            raw_matcounts =per_ascension_data['cost']

            ascension_mats_per_level = []
            for raw_matcount in raw_matcounts:
                mat_id = raw_matcount['id']

                from hsr_client.backend.srs_backend.parsers.material import parse_material
                mat = parse_material(mat_id, self._backend)
                
                
                mat_count = raw_matcount['count']

                ascension_mats_per_level.append(
                    MaterialCount(
                    material=mat,
                    count = mat_count,
                    )
                )
            ascension_mats[level] = ascension_mats_per_level

        return ascension_mats
    
    def skills(self) -> List[Skill]:
        """Returns a List of `Skill`s that the character posseses"""
        # skills
        skills = []
        
        raw_skills = self._chara_skills


        for raw_skill in raw_skills:
            # name
            skill_name = raw_skill['name']

            # scaling: LevelScaling
                        

            scaling = {}
            for level, level_data in enumerate(raw_skill['levelData'], start=1):

                desc_template = BeautifulSoup(
                    raw_skill["descHash"], features="lxml"
                ).get_text()

                template_params = level_data['params']

                skill_desc = desc_template
                for slot_no, template_param in enumerate(template_params, start=1):
                    replace_text = f"#{slot_no}[i]"
                    # print("replacing: " + replace_text + " with " + str(template_param) + " in " + ability_desc)
                    skill_desc = skill_desc.replace(replace_text, str(template_param))

                

                raw_matcounts =level_data['cost']

                upgrade_mats_per_level = []
                for raw_matcount in raw_matcounts:
                    mat_id = raw_matcount['id']

                    from hsr_client.backend.srs_backend.parsers.material import parse_material
                    mat = parse_material(mat_id, self._backend)
                    
                    
                    mat_count = raw_matcount['count']

                    upgrade_mats_per_level.append(
                        MaterialCount(
                        material=mat,
                        count = mat_count,
                        )
                    )

                scaling[level] = trace.LevelScaling(
                    upgrade_mats=upgrade_mats_per_level,
                    description=skill_desc
                )

            skills.append(
                Skill(
                    name=skill_name,
                    scaling=scaling,
                )
            )
        return skills

