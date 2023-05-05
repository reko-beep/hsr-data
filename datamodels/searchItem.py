from pydantic import BaseModel, validator, Field
from typing import Optional



class SearchItem(BaseModel):

    url : str
    iconPath : str
    type : int
    name : str
    rarity : int

    
