
from typing import Optional, Union, List, NewType
from pydantic import BaseModel

class Eidolon(BaseModel):
    """Character's Eidolon"""
    # eidolon name
    name : str
    # eidolon number.
    number: int
    # eidolon description.
    description: Optional[str]
    # TODO: add eidolon icon property.