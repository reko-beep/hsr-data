import re
import data_query.shared_data.shared_var as SharedVar
from data_query.query_errors.errors import SkillLevelOutOfRange


def get_skillparams_onlevel(typeDesc: str, level: int, current_skill) -> dict | None:  # type: ignore
    get_skill_category: dict | None = current_skill
    if get_skill_category is not None:
        levelData: dict = get_skill_category["levelData"]
        max_level: int = len(levelData)
        if level > max_level:
            raise SkillLevelOutOfRange
        else:
            for params in levelData:
                if params["level"] == level:
                    return params
    else:
        return None


def get_typeDescHash(get_data, skill_data) -> dict | None:  # type: ignore
    for data in skill_data:
        if data["typeDescHash"] == get_data:
            return data


def skill_general(typeDesc: str, level: int, skill_data) -> str | None:
    current_skill = get_typeDescHash(typeDesc, skill_data)
    get_skill_onlevel = get_skillparams_onlevel(typeDesc, level, current_skill)
    if get_skill_onlevel is not None:
        get_skill_params = get_skill_onlevel["params"]
        skill_params: list[float] = get_skill_params
        if current_skill is not None:
            atktype: str = current_skill["tagHash"]
            descHash: str = current_skill["descHash"]
            return SharedVar.readable_descHash(
                typeDesc, skill_params, descHash, level, typeDesc
            )
        else:
            return None
    else:
        return None
