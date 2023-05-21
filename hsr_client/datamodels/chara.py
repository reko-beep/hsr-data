
from typing import List, Optional
from pydantic import BaseModel, PrivateAttr

from hsr_client.datamodels.eidolon import Eidolon
from hsr_client.datamodels.element import Element
from . import trace
from hsr_client.paths import Path

from enum import Enum


class Stats(BaseModel):
    ATK: float
    HP: float
    DEF: float
    CRIT: float
    CDMG: float
    SPD: float


# TODO: decide all the parameters
class Character(BaseModel):
    """Traces possessed by the `Character`"""
    name: str
    """Name of the Character"""
    rarity: int
    """Rarity of the Character"""
    element: Element
    """Element of the Character"""
    description: str
    """short description about the character."""
    path: Path
    """Path followed by the Character`"""
    eidolons: List[Eidolon]
    """Character's Eidolons"""
    traces: list[trace.Trace]
    """Character's Traces"""


    _stats = PrivateAttr()



    def stats(self, level, ascended=False) -> Stats:
        # TODO: implemented this
        pass

