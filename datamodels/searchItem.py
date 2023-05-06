from pydantic import BaseModel, validator, Field, Extra
from typing import Optional
from routes import IMAGE_ROUTE
from constants import Types


class SearchItem(BaseModel):

    url : Optional[str]
    iconPath : Optional[str]
    type : Optional[int]
    name : Optional[str]
    rarity : Optional[int]
    id : int | str

    class Config:
        extra = Extra.allow

    @validator('iconPath', pre=True)
    def get_icon_url(cls, v):
        return IMAGE_ROUTE.format(assetId=v)

    @validator('type', pre=True)
    def get_item_type(cls, v):
        if isinstance(v, int) and v < 7:
            return Types(v)
        
    
  
    