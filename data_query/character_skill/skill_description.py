import re
import data_query.shared_data.shared_var as SharedVar
from typing import Dict, List
from data_query.query_errors.errors import SkillLevelOutOfRange


def get_skillparams_onlevel(typeDesc: str, level: int, current_skill) -> Dict:
    get_skill_category: Dict | None = current_skill
    if get_skill_category is not None:
        levelData: List = get_skill_category["levelData"]
        max_level: int = len(levelData)
        if level > max_level:
            raise SkillLevelOutOfRange
        else:
            for params in levelData:
                if params["level"] == level:
                    return params


def get_typeDescHash(get_data, skill_data) -> Dict | None:
    for data in skill_data:
        if data["typeDescHash"] == get_data:
            return data


def skill_general(typeDesc: str, level: int, skill_data):
    current_skill: Dict | None = get_typeDescHash(typeDesc, skill_data)
    skill_params: List[float] = get_skillparams_onlevel(typeDesc, level, current_skill)[
        "params"
    ]
    if current_skill is not None:
        atktype: str = current_skill["tagHash"]
        descHash: str = current_skill["descHash"]
        descHash_cleaned: str = re.sub("<[^\>]+.", "", descHash)
        return SharedVar.readable_descHash(
            typeDesc, skill_params, descHash_cleaned, level
        )
