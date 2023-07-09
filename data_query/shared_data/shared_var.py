from typing import List, Tuple
from itertools import count


class SharedVar:
    @staticmethod
    def level() -> List[int]:
        level_iterator: count = count(start=20, step=10)
        level_list: List = list(next(level_iterator) for _ in range(7))
        return level_list

    @staticmethod
    def skill_description(
        typeDesc: str, skill_params: List[float], deschash_cleaned: str, level: int
    ) -> str:
        value_params: Tuple = tuple(
            f"{value * 100:.1f}" if isinstance(value, float) else str(value)
            for value in skill_params
        )
        descHash_list: List = []
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
