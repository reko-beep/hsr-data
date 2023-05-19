from enum import Enum


O_VALUE = "6b14cd54ea92edd2dbfc20fa8b0d5797"  # idk site changes this a lot


class Item(int, Enum):
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
