
from typing import Optional
from pydantic import BaseModel, validator, Field, Extra

from enum import Enum

class Type(Enum):
    """type of trace (Stat Bonus, Skill, Bonus Ability)"""
    BONUS_ABILITY = 1
    STAT_BONUS = 2
    SKILL = 3


class UnlockCriteria(BaseModel):
    """criteria to satisfy before this trace can be unlocked."""
    # character ascension required.
    ascension: Optional[int]
    # character level required
    level: Optional[int]
    # trace to be unlocked before.
    trace: Optional['Trace']
  
    



# TODO: decide all the parameters
class Trace(BaseModel):
    """Traces possessed by the `Character`"""
    # name of the trace.
    name : str
    # type of trace.
    type : Type
    # description of the trace.
    description: Optional[str]
    # criteria to satisfy before this trace can be unlocked.
    unlock_criteria: Optional[UnlockCriteria]
    # trace level.
    level: Optional[int]

UnlockCriteria.update_forward_refs()


