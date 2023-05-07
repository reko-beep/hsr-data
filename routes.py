
from constants import O_VALUE


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

    def __init__(self, file: str) -> None:
        self.file = file
        self.path = f"{file.replace('.json','/',1)}"    

    def generate_goto_lang_path(self, lang: str):
        return f'{lang}/{self.path}'

    def generate_main_lang_path(self, lang: str):
        return f"{lang}/{self.file}"


SEARCH = Routes('searchItems.json')
CHARACTERS = Routes('characters.json')
EQUIPMENT = Routes('equipment.json')
RELICS = Routes('relics.json')
MATERIALS = Routes('materials.json')
BOOKS = Routes('books.json')
CONSUMABLES = Routes('foods.json')
PLAYERCARDS = Routes('playercards.json')
ROGUES = Routes('rogues.json')

