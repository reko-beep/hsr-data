
from enum import Enum


O_VALUE = '6b14cd54ea92edd2dbfc20fa8b0d5797' # idk site changes this a lot

class Types(int, Enum):

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

    ENG = 'en'
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

    BODY = 'Body'
    FEET = 'Feet'
    PLANAR_SPHERE = 'Planar Sphere'
    LINK_ROPE = 'Link Rope'
    HANDS = 'Hands'

    def __str__(self) -> str:
        return str(self.value)
