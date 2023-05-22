
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
    TAUNT: float


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
        """
        Get Character's Stats for the given level. when `ascended=True` is used
        on levels that can cap, gives `Stats` for ascended levels instead.
        """
        if level < 1 or level > 80: # TODO: or is this 90?
            raise ValueError(" 1 <= level <= 80 criteria not satisfied.")
        
        for ascension_entry in self._stats:
            if level <= ascension_entry["maxLevel"]:
                if ascension_entry["maxLevel"] == level and ascended == True:
                    continue
                
                return Stats(
                    ATK=ascension_entry["attackBase"] + ascension_entry["attackAdd"] * (level - 1),
                    HP=ascension_entry["hpBase"] + ascension_entry["hpAdd"] * (level - 1),
                    DEF=ascension_entry["defenseBase"] + ascension_entry["defenseAdd"] * (level - 1),
                    SPD=ascension_entry["speedBase"] + ascension_entry["speedAdd"] * (level - 1),
                    CRIT=ascension_entry["crate"] * 100,
                    CDMG=ascension_entry["cdmg"] * 100,
                    TAUNT=ascension_entry["aggro"],
                )
