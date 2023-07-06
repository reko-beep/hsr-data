from typing import List
from itertools import count


class SharedVar:
    @staticmethod
    def level() -> List[int]:
        level_iterator: next = count(start=20, step=10)
        level_list: List = list(next(level_iterator) for _ in range(7))
        return level_list
