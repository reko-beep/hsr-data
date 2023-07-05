
from typing import Optional, Union, List, NewType
from pydantic import BaseModel

class Eidolon(BaseModel):
    """Character's Eidolon"""
    # eidolon name
    name : str
    """Eidolon's Name"""
    resonance: int
    """Eidolon Number/Resonance/Rank"""
    description: Optional[str]
    """Eidolon short description."""
    # TODO: add eidolon icon property.