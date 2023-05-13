from typing import Dict, List, NewType, Tuple, Iterable
from pydantic import BaseModel
from hsr_client.datamodels.material import Material
from hsr_client.stats import Stats
from hsr_client.paths import Path

class Stats(BaseModel):
    ATK: int
    HP: int
    DEF: int

Level = int
Count = int
Superimposition = int


class AscensionMaterial(BaseModel):

    material: Material
    count: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __iter__(self):
        return iter(self.mats)




class Lightcone(BaseModel):
    """
    Lightcone
    
   Attributes:
        name: name of the lightcone
        description: description of the lightcone
        path: Path association of the Lightcone
        scaling: lightcone scaling by level. key: level, value: Stats
        ability: lightcone ability description for given superimposition (int)
        ascension_mats: ascension materials required to level up beyond given `Level` (int)
    """
    name: str
    # ligthcone rarity
    rarity: int
    description: str
    path: Path
    # lightcone stats scaling by `Level` (int)
    stats: Dict[Level, Stats]
    # lightcone ability description for given `Superimposition` (int)
    ability: Dict[Superimposition, str]

    # TODO: type too long? should we break it down?
    # ascension materials required to level up beyond given `Level` (int)
    ascension_mats: Dict[Level, List[Dict[Material, Count]]]


if __name__ == "__main__":

    lightcone = Lightcone(
        name="light cone",
        rarity=4,
        description="this is a light cone , and this is its history",
        path = Path.Harmony,
        stats = {
            1: Stats(
                ATK=12,
                HP=13,
                DEF=14,
            )
        },
        ability={
            1: "at superimposition level damage bonus is 30%"
        },
        ascension_mats={
        20: [
            {Material(name="foo1", description="bar1"): 1},
            {Material(name="foo2", description="bar2"): 2}
        ],
        30: [
            {Material(name="foo3", description="bar3"): 3}
        ]
    })

    lvl_20_ascension_mats = lightcone.ascension_mats[20] # TODO: this doesn't read well. what does ascension_mats[20] mean, unless u look at the type.

    for mats in lvl_20_ascension_mats:
        print("mats:" , mats.keys())
        print("count: ", mats.values())