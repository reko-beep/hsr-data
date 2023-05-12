
from constants import O_VALUE
from datetime import datetime, date

MAIN_ROUTE = f'https://starrailstation.com/api/v1/data/{O_VALUE}/'
IMAGE_ROUTE = 'https://starrailstation.com/assets/{assetId}.webp'
AUDIO_ROUTE = 'https://starrailstation.com/assets/{assetId}.mp3'


class Routes:
    '''
    This class is meant to convert json files
    to routes for navigating or going to specific Item

    ---
    example:
    ---
    
    - main path is en/characters.json
    - goto path is en/characters/id.json
    
    '''

    def __init__(self, file: str, path: str = '') -> None:
        self.file = file
        self.path = path

        if self.path == '':
            self.path = f"{file.replace('.json','/',1)}"    

    def generate_goto_lang_path(self, lang: str):
        return f'{lang}/{self.path}'

    def generate_main_lang_path(self, lang: str):
        return f"{lang}/{self.file}"


SEARCH = Routes(file='searchItems.json', path='materials/')
CHARACTERS = Routes(file='characters.json')
EQUIPMENT = Routes(file='equipment.json', path='materials/')
RELICS = Routes(file='relics.json')
MATERIALS = Routes(file='materials.json')
BOOKS = Routes('books.json')
CONSUMABLES = Routes('foods.json', path='materials/')
PLAYERCARDS = Routes('playercards.json', path='materials/')
LIGHTCONES = Routes('lightcones.json')
ACHIEVEMENTS = Routes(file='achievements.json', path=None)

'''
not month safe calculation for now

'''
CURRENT_DATE  = datetime.now().date()
ROUGE_DIFF_DATE = 0 - CURRENT_DATE.weekday()
ROUGE_DATE =  date(CURRENT_DATE.year, CURRENT_DATE.month, CURRENT_DATE.day + (ROUGE_DIFF_DATE) )


ROUGES = Routes(file=f'rogue/{str(ROUGE_DATE)}.json', path=f'rogue/{str(ROUGE_DATE)}.json') #idk site has rogue spelling

