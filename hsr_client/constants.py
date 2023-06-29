from enum import Enum, IntEnum


O_VALUE = "831f36f73549d1d18a12937d98be4c56"  # idk site changes this a lot


class Item(IntEnum):
    """
    Search Item types

    """

    CHARACTER = 0
    LIGHTCONE = 1
    RELIC = 2
    BOOK = 3
    MATERIAL = 4
    PLAYERCARD = 5
    FOOD = 6

    def __str__(self) -> int:
        return self.value


class Language(str, Enum):
    """

    Allowed languages
    """

    EN = "en"
    CN = "cn"
    DE = "de"
    ES = "es"
    FR = "fr"
    ID = "id"
    JP = "jp"
    KR = "kr"
    PT = "pt"
    RU = "ru"
    TH = "th"

    def __str__(self) -> str:
        return str(self.value)


class _RelicTypes(str, Enum):
    """
    Relic Types
    """

    BODY = "Body"
    FEET = "Feet"
    PLANAR_SPHERE = "Planar Sphere"
    LINK_ROPE = "Link Rope"
    HANDS = "Hands"

    def __str__(self) -> str:
        return str(self.value)


class MaterialTypes(int, Enum):
    """
    Material Types   
    """

    CHARACTER_EXP_MATERIALS = 1
    CHARACTER_ASCENSION_MATERIALS = 2
    TRACE_MATERIAL_LIGHTCONE_ASCENSION_MATERIALS = 3    
    TRACE_MATERIALS = 4
    LIGHTCONE_EXP_MATERIALS = 5
    RELIC_EXP_MATERIALS = 6
    TRACE_MATERIAL_CHARACTER_ASCENSION_MATERIALS = 7
    WARP_ITEM = 8
    LIMITED_WARP_ITEM = 9
    CONSUMABLES = 10
    COMMON_CURRENCY = 11
    RARE_CURRENCY = 12
    WORLD_CURRECNY = 13
    VALUABE_OBJECT = 14
    RELIC_COFFRET = 15
    SYNTHESIS_MATERIAL = 17
    RECIPE = 17
