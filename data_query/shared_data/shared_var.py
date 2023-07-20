from typing import List, Tuple
from itertools import count
import re


def level() -> List[int]:
    level_iterator: count = count(start=20, step=10)
    level_list: List = list(next(level_iterator) for _ in range(7))
    return level_list


def readable_descHash(
    typeDesc: str, skill_params: List[float], desc: str, level: int | str, output=None
) -> str | None:
    char_skill = [
        "Basic ATK",
        "Skill",
        "Ultimate",
        "Talent",
        "Technique",
        "lightcone",
        "trace",
    ]
    value_params: Tuple = tuple(
        f"{value * 100:.1f}" if isinstance(value, float) and value < 4.0 else str(value)
        for value in skill_params
    )
    deschash_cleaned: str = re.sub("<[^\>]+.", "", desc)
    descHash_list: List = []
    if "[f1]" in deschash_cleaned:
        deschash_cleaned = deschash_cleaned.replace("[f1]", "[i]")
    if "#1[i]" not in deschash_cleaned:
        if output in char_skill:
            return f"{typeDesc} Lv.{level}: {deschash_cleaned}"
        elif output == "relic":
            return f"{typeDesc} {level}-set: {deschash_cleaned}"
        elif output == "constellation":
            return f"{typeDesc}: {deschash_cleaned}"
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
        return correct_punctuations(f"{typeDesc} Lv.{level}: {descHash_list[-1]}")
    elif output == "relic":
        return f"{typeDesc} {level}-set: {descHash_list[-1]}"
    elif output == "constellation":
        return f"{typeDesc}: {descHash_list[-1]}"
    else:
        return None


def correct_punctuations(readable_deschashes, output=None) -> str:
    default = re.sub(r"([\.!,:;?])([a-zA-Z])", r"\g<1> \g<2>", readable_deschashes)
    if output is None:
        return default
    elif output == "constellation":
        const = re.sub(r"([\.])\s([+?\d])", r"\g<1>\g<2>", default)
        return const
    else:
        pass


def readable_deschash_text(deschash) -> str:
    return re.sub("<[^\>]+.", "", deschash)
