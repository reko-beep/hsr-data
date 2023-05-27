from typing import Dict, List, NewType, Tuple, Iterable
from pydantic import BaseModel, PrivateAttr
from hsr_client.datamodels.material import Material, MaterialCount
from hsr_client.hsr_types import  Superimposition, Level
from hsr_client.paths import Path

class Stats(BaseModel):
    """
    Lightcone's base stats
    """
    ATK: int
    """Lightcone base ATK"""
    HP: int
    """Lightcone base HP"""
    DEF: int
    """Lightcone DEF"""







class Lightcone(BaseModel):
    """
    Model to represent a Lightcone



    Attributes:

        - name: name of the lightcone
        - description: description of the lightcone
        - path: Path association of the Lightcone
        - ability: lightcone ability description for given superimposition (int)
        - ascension_mats: ascension materials required to level up beyond given `Level` (int)

    """

    name: str
    "name of the lightcone"
    rarity: int
    """rarity of the lightcone"""
    description: str
    """short description of the lightcone"""
    path: Path
    """Path association of the lightcone"""



    # directly using starrail station's `levelData` structure here. since `Stats`
    # going to be accessed only via a function anyway.
    # offering it via an instance variable like `stats` would be unncessarily big
    # listing. of `Stats` for level 1 through 80
    # offering a function instead will also feature proof the model
    # since no public attribute is exposed now, that will change later.
    # only downside I can think of is, if the user wants to save the 
    # model via json() etc., the stats wont be a part of it.
    # but i feel limitation is better than making breaking change.
    _stats = PrivateAttr()
    
    # # lightcone stats scaling by `Level` (int)
    # stats: Dict[Level, Stats]
    
    

    ability: Dict[Superimposition, str]
    """lightcone ability description for given `Superimposition (int)`"""
    # ascension materials required to level up beyond given `Level` (int)
    ascension_mats: Dict[Level, List[MaterialCount]]
    """ascension mats required to level up beyond the given `Level (int)` """

    def stats(self, level: Level, ascended=False):
        """
        Get Ligthcone's Stats for the given level. when ascended=True is used
        on levels where ascension is possible, gives `Stats` for ascended levels
        instead.
        """
        if level < 1 or level > 80:
            raise ValueError(" 1 <= level <= 80 criteria not satisfied.")
        
        for ascension_entry in self._stats:
            if level <= ascension_entry["maxLevel"]:
                if ascension_entry["maxLevel"] == level and ascended == True:
                    continue
                
                return Stats(
                    ATK=ascension_entry["attackBase"] + ascension_entry["attackAdd"] * (level - 1),
                    HP=ascension_entry["hpBase"] + ascension_entry["hpAdd"] * (level - 1),
                    DEF=ascension_entry["defenseBase"] + ascension_entry["defenseAdd"] * (level - 1),
                )

         

     






if __name__ == "__main__":

    

    lightcone = Lightcone(
        name="light cone",
        rarity=4,
        description="this is a light cone , and this is its history",
        path = Path.HARMONY,
        ability={
            1: "at superimposition level damage bonus is 30%"
        },
        ascension_mats={
        20: [
            MaterialCount(material=Material(name="foo1", description="bar1", rarity=4, source=["somewhere"], lore="nice lore"), count=1),
            MaterialCount(material=Material(name="foo2", description="bar2", rarity=4, source=["somewhere"], lore="nice lore"), count=2),
        ],
        30: [
            MaterialCount(material=Material(name="foo3", description="bar3", rarity=4, source=["somewhere"], lore="nice lore"), count=3),
        ]
    })

    import json
    setattr(lightcone, "_stats", json.loads("""
    [
    {
        "promotion": 0,
        "maxLevel": 20,
        "cost": [
            {
                "id": 29328,
                "count": 3000
            },
            {
                "id": 549437,
                "count": 4
            }
        ],
        "attackBase": 14.4,
        "attackAdd": 2.16,
        "hpBase": 38.4,
        "hpAdd": 5.76,
        "defenseBase": 12,
        "defenseAdd": 1.8
    },
    {
        "promotion": 1,
        "maxLevel": 30,
        "cost": [
            {
                "id": 29328,
                "count": 6000
            },
            {
                "id": 635674,
                "count": 2
            },
            {
                "id": 549437,
                "count": 8
            }
        ],
        "attackBase": 31.68,
        "attackAdd": 2.16,
        "hpBase": 84.48,
        "hpAdd": 5.76,
        "defenseBase": 26.4,
        "defenseAdd": 1.8
    },
    {
        "promotion": 2,
        "maxLevel": 40,
        "cost": [
            {
                "id": 29328,
                "count": 12000
            },
            {
                "id": 920201,
                "count": 2
            },
            {
                "id": 633378,
                "count": 4
            }
        ],
        "attackBase": 54.72,
        "attackAdd": 2.16,
        "hpBase": 145.92,
        "hpAdd": 5.76,
        "defenseBase": 45.6,
        "defenseAdd": 1.8
    },
    {
        "promotion": 3,
        "maxLevel": 50,
        "cost": [
            {
                "id": 29328,
                "count": 30000
            },
            {
                "id": 920201,
                "count": 4
            },
            {
                "id": 633378,
                "count": 6
            }
        ],
        "attackBase": 77.76,
        "attackAdd": 2.16,
        "hpBase": 207.36,
        "hpAdd": 5.76,
        "defenseBase": 64.8,
        "defenseAdd": 1.8
    },
    {
        "promotion": 4,
        "maxLevel": 60,
        "cost": [
            {
                "id": 29328,
                "count": 60000
            },
            {
                "id": 836260,
                "count": 3
            },
            {
                "id": 717319,
                "count": 3
            }
        ],
        "attackBase": 100.8,
        "attackAdd": 2.16,
        "hpBase": 268.8,
        "hpAdd": 5.76,
        "defenseBase": 84,
        "defenseAdd": 1.8
    },
    {
        "promotion": 5,
        "maxLevel": 70,
        "cost": [
            {
                "id": 29328,
                "count": 120000
            },
            {
                "id": 836260,
                "count": 6
            },
            {
                "id": 717319,
                "count": 5
            }
        ],
        "attackBase": 123.84,
        "attackAdd": 2.16,
        "hpBase": 330.24,
        "hpAdd": 5.76,
        "defenseBase": 103.2,
        "defenseAdd": 1.8
    },
    {
        "promotion": 6,
        "maxLevel": 80,
        "cost": [],
        "attackBase": 146.88,
        "attackAdd": 2.16,
        "hpBase": 391.68,
        "hpAdd": 5.76,
        "defenseBase": 122.4,
        "defenseAdd": 1.8
    }
]
    """))

    lvl_20_ascension_mats = lightcone.ascension_mats[20] # TODO: this doesn't read well. what does ascension_mats[20] mean, unless u look at the type.



    print(lightcone.stats(20, ascended=True))


