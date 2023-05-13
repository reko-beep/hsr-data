from typing import Dict, List, Tuple
from pydantic import BaseModel
from datamodels.material import Material
from hsr_client.stats import Stats
from paths import Path

class Stats(BaseModel):
    ATK: int
    HP: int
    DEF: int



class Scaling(BaseModel):
    """light cone scaling for a given level."""
    upgrade_mats: List[Tuple[Material, int]]
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

