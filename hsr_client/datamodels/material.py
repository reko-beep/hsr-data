from pydantic import BaseModel
from typing import Optional, Dict



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
    type: int


    # material rarity
    rarity : int

    #material description
    description : str

    # material lore
    lore : Optional[str]
      
    # TODO: determine icon stratergy
    # is it image, or url or what?


        
#     obtain : Optional[list[str]]
#     '''
#     usage should contain both equipment and  characters
#     either it can be both or one or empty
#     '''

#     usage: Optional[Dict[str , list]]


   
