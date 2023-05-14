from pydantic import BaseModel
from typing import Optional, Dict


#TODO: model is loosely based on data from star rail station, need to compare with hoyolab data.



class Material(BaseModel):
    """Material Model

    Attributes:
        id : id of material.
        name: name of the material.
        type: type of material, character exp, playercard, consumable etc.
        iconPath: url of the material icon.
        rarity: rarity of the material.
        description : description of the material.
        lore : lore of the material, if it has any attached to it.
        obtain: list of locations , route, shops where you can get the material from.
        usage: material consumed or used by equipment or character in ascension, boost or upgrade. {'character': [], 'equipment' : []}
    """       

    id : int
    name : str
    type: int

    # icon path to be made or completed in parsers object
    iconPath : str

    # material rarity
    rarity : int

    #material description
    description : str

    # material lore
    lore : Optional[str]
        
    obtain : Optional[list[str]]
    '''
    usage should contain both equipment and  characters
    either it can be both or one or empty
    '''

    usage: Optional[Dict[str , list]]

    
    
