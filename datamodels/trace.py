from pydantic import BaseModel, validator, Field, Extra
from typing import Optional
from enum import Enum


class Type(Enum):
    BONUS_ABILITY = 1
    STAT_BONUS = 2
    SKILL = 3

class UnlockCriteria(BaseModel):
    ascension: int
    level: int
    # mats: 


# type 1: "Bonus Ability"
# type 2: "Stat Bonus"
class Trace(BaseModel):

    name : str
    type : Type
    description: str
    unlock_criteria: UnlockCriteria
    level: Optional[int]


if __name__ == "__main__":

    import json
    with open("test/single_trace.json") as f:
        trace_data = json.load(f)

        for trace in trace_data:

            ...

def parse_trace_data(data, traces=[]) -> list[Trace]:

    pass


def get_trace_name(data):
    trace_name = None
    containers = ["embedBuff", "embedBonusSkill"]

    for container in containers:

        try:
            trace_name = data[container]["name"]
        except KeyError:
            continue

    if trace_name is not None:
        return trace_name
    else:
        raise ValueError