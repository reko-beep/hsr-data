
from typing import Optional, Union, List, NewType, Tuple
from pydantic import BaseModel, validator, Field, Extra, ValidationError

from enum import Enum

from hsr_client.datamodels.lightcone import MaterialCount
from hsr_client.datamodels.material import Material



class UnlockPrerequisite(BaseModel):
    """criteria to satisfy before this trace can be unlocked."""
    # character ascension required.
    ascension: Optional[int]
    # character level required
    level: Optional[int]
    # trace to be unlocked before.
    trace: Optional['Trace']
  
    

class BonusAbility(BaseModel):
    # name of the trace.
    name : str
    # description of the trace.
    description: Optional[str]



    # list of materials required to activate the trace.
    activation_mats: List[MaterialCount]
    # criteria to satisfy before this trace can be unlocked.
    unlock_prerequisite: Optional[UnlockPrerequisite]


    # @validator
    # def ensure_level_one(cls, level):
    #     if level is not 1:
    #         raise ValidationError("Bonus Ability's level can only be equal to 1")

# StatBonus = NewType('StatBonus', BonusAbility)
class StatBonus(BonusAbility):
    pass

class LevelScaling(BaseModel):
    level: int
    upgrade_mats: List[Tuple[Material, int]]
    description: str
    

# TODO: decide all the parameters
class Skill(BaseModel):
    """Traces possessed by the `Character`"""
    # name of the trace.
    name : str
    # how the trace scales with level
    level_scaling: LevelScaling

Trace = Union[Skill, StatBonus, BonusAbility]
   



UnlockPrerequisite.update_forward_refs()


