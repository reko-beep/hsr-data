from typing import List, Tuple
from itertools import count


def level() -> List[int]:
    level_iterator: count = count(start=20, step=10)
    level_list: List = list(next(level_iterator) for _ in range(7))
    return level_list


def readable_descHash(
    typeDesc: str, skill_params: List[float], deschash_cleaned: str, level: int | str
) -> str:
    value_params: Tuple = tuple(
        f"{value * 100:.1f}" if isinstance(value, float) else str(value)
        for value in skill_params
    )
    descHash_list: List = []
    if "#1[i]" not in deschash_cleaned:
        return f"{typeDesc} Lv.{level}: {deschash_cleaned}"
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
    return f"{typeDesc} Lv.{level}: {descHash_list[-1]}"
