from typing import List, Tuple
from itertools import count
import re


def level() -> List[int]:
    level_iterator: count = count(start=20, step=10)
    level_list: List = list(next(level_iterator) for _ in range(7))
    return level_list


def readable_descHash(
    typeDesc: str, skill_params: List[float], desc: str, level: int | str, output=None
) -> str:
    char_skill = [
        "Basic ATK",
        "Skill",
        "Ultimate",
        "Talent",
        "Technique",
        "constellation",
        "lightcone",
    ]
    value_params: Tuple = tuple(
        f"{value * 100:.1f}" if isinstance(value, float) else str(value)
        for value in skill_params
    )
    deschash_cleaned: str = re.sub("<[^\>]+.", "", desc)
    descHash_list: List = []
    if "#1[i]" not in deschash_cleaned:
        if output in char_skill:
            return f"{typeDesc} Lv.{level}: {deschash_cleaned}"
        elif output == "relic":
            return f"{typeDesc} {level}-set: {deschash_cleaned}"
        else:
            pass
    for index in range(len(skill_params)):
        if len(descHash_list) == 0:
            descHash_first: str = deschash_cleaned.replace(
                f"#{index + 1}[i]", value_params[index]
            )
            descHash_list.append(descHash_first)
        else:
            descHash_next: str = descHash_list[index - 1].replace(
                f"#{index + 1}[i]", value_params[index]
            )
            descHash_list.append(descHash_next)
    if output in char_skill:
        return f"{typeDesc} Lv.{level}: {descHash_list[-1]}"
    elif output == "relic":
        return f"{typeDesc} {level}-set: {descHash_list[-1]}"
    else:
        pass
