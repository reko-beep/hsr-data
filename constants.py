
from enum import Enum


O_VALUE = '6b14cd54ea92edd2dbfc20fa8b0d5797' # idk site changes this a lot

class Types(int, Enum):

    CHARACTERS = 0
    LIGHTCONES = 1
    RELICS = 2
    BOOKS = 3
    MATERIALS = 4
    FOODS = 6
    PLAYERCARDS = 5

    