from enum import Enum



class Item(str, Enum):
    
    '''
    HoYoLab Wiki Entries
    Item | Codes

    - PATHS : 102
    - CHARACTERS : 104
    - NPCS : 105
    - LIGHTCONES : 107
    - RELICS : 108
    - MATERIALS : 110
    - MUSIC_DISKS : 117
    - ENEMIES : 112
    '''
    
    PATHS = '102'
    CHARACTERS = '104'
    NPCS = '105'
    LIGHTCONES = '107'
    RELICS = '108'
    MATERIALS = '110'
    MUSIC_DISKS = '117'
    ENEMIES = '112'

    def __str__(self) -> str:
        return str(self.value)