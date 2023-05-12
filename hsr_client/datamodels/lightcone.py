from typing import Dict, Optional, Union, List, NewType
from pydantic import BaseModel, validator, Field, Extra, ValidationError
from datamodels.material import Material
from stats import Stats
from paths import Path

class Stats(BaseModel):
    ATK: int
    HP: int
    DEF: int



class Scaling(BaseModel):
    """light cone scaling for a given level."""
    upgrade_mats: List[(Material, int)]
    description: str

class Lightcone(BaseModel):
    """
    Lightcone
    
   Attributes:
        name: name of the lightcone
        description: description of the lightcone
        level_scaling: lightcone scaling by leve. {level: Scaling}
    """
    name: str
    description: str
    stats: Stats
    path: Path
    # lightcone scaling by level. `{level: Scaling}`
    level_scaling: Dict[int, Scaling]
    superimposition: 
