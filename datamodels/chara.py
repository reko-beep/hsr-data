
from typing import Optional
from pydantic import BaseModel
from . import trace

from enum import Enum


class Type(Enum):
    """type of trace (Stat Bonus, Skill, Bonus Ability)"""
    BONUS_ABILITY = 1
    STAT_BONUS = 2
    SKILL = 3



# TODO: decide all the parameters
class Character(BaseModel):
    """Traces possessed by the `Character`"""
    # name of the trace.
    name: str
    traces: list[trace.Trace]



