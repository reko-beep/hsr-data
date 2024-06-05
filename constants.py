
from enum import Enum


O_VALUE = 'a179bc7f408c16403ad6db83281cda00' # idk site changes this a lot

class Types(int, Enum):
    '''
    Search Item types
    
    '''

    CHARACTERS = 0
    LIGHTCONES = 1
    RELICS = 2
    BOOKS = 3
    MATERIALS = 4    
    PLAYERCARDS = 5
    FOODS = 6

    def __str__(self) -> int:
        return self.value


class Languages(str, Enum):
    '''
    
    Allowed languages
    '''

    EN = 'en'
    CN = 'cn'
    DE = 'de'
    ES = 'es'
    FR = 'fr'
    ID = 'id'
    JP = 'jp'
    KR = 'kr'
    PT = 'pt'
    RU = 'ru'
    TH = 'th'

    def __str__(self) -> str:
        return str(self.value)

class RelicTypes(str, Enum):
    '''
    Relic Types
    '''

    BODY = 'Body'
    FEET = 'Feet'
    PLANAR_SPHERE = 'Planar Sphere'
    LINK_ROPE = 'Link Rope'
    HANDS = 'Hands'

    def __str__(self) -> str:
        return str(self.value)
