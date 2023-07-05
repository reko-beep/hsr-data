from pydantic import BaseModel, validator, Field, Extra
from typing import Optional, Union, Literal
from hsr_client.routes import IMAGE_ROUTE
from hsr_client.constants import Item
from hsr_client.backend.hoyo_backend.constants import Item as HoyoItems


class SearchItem(BaseModel):
    """SearchItem

    Attributes:

    url : site url for item
    iconPath : icon url of the  item
    type: type of item - lightcones, materials, characters
    rarity: rarity of the item
    id : ID of the item

    Filters:

        - available_filters()
            to see the attributes you can filter item on


    """

    url: Optional[str]
    iconPath: Optional[str]
    type: Union[HoyoItems, Item]
    name: Optional[str]
    rarity: Optional[int]
    id: Union[int, str]

    class Config:
        extra = Extra.allow

    def available_filters(self):
        """TODO: add documentation here"""

        return [f for f in self.__dict__.keys() if f not in ["url", "iconPath", "id"]]

    @validator('type', pre=True)
    def get_correct_type(cls, v):

        if isinstance(v, str):
            v = int(v)        
        if v > 100:
            return HoyoItems(v)
        else:
            return Item(v)
        

    def __str__(self):
        if self.type > 50:
            return str(
                f"<{HoyoItems(str(self.type)).name} name={self.name} rarity={self.rarity} iconPath={self.iconPath}>"
            )
        return str(
            f"<{Item(self.type).name} name={self.name} rarity={self.rarity} iconPath={self.iconPath}>"
        )

    def __repr__(self):
        if self.type > 50:
            return str(
                f"<{HoyoItems(str(self.type)).name} name={self.name} rarity={self.rarity} iconPath={self.iconPath}>"
            )
        return str(
            f"<{Item(self.type).name} name={self.name} rarity={self.rarity} iconPath={self.iconPath}>"
        )
