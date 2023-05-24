from pydantic import BaseModel, PrivateAttr
from typing import Optional, Dict, List









#     MODIFICATION NOTES: obtain will be replaced by source. which can be a type of its own.
#            iconPath is starrail specific. need something more general that fits with hoyolab aswell
#            id has no place as a visible attribute, maybe it can be an internal attribute for reference purpose
#            but the api doesn't flow backwards, most of the time, so need to think if ID is even necessary.
#            Ofcourse it might still be needed, just shouldn't be a part of public api.

class Material(BaseModel):

    """Material Model

    Attributes:
        name: name of the material.
        type: type of material, character exp, playercard, consumable etc.
        rarity: rarity of the material.
        description : description of the material.
        lore : lore of the material, if it has any attached to it.
        obtain: list of locations , route, shops where you can get the material from.
        usage: material consumed or used by equipment or character in ascension, boost or upgrade. {'character': [], 'equipment' : []}
    """       

 
    name : str
    # type: int


    rarity : int
    """Rarity of the Material"""
    description : str
    """Description of the Material"""
    lore : Optional[str]
    """Lore/Notes/Comments on the Material"""      
    # TODO: determine icon stratergy
    # is it image, or url or what?

    # This will be a string for now. maybe own type later? 
    # i don't find any use for now.
    source: List[str]
    """Where to obtain the Material"""
        
   
    _meta = PrivateAttr()




class MaterialCount(BaseModel):
    material: Material
    count: int
