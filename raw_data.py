from main import SRSClient
from hsr_client.constants import Item, Language
from hsr_client.routes import *
from os import getcwd, mkdir
from os.path import exists

from json import dump
from time import sleep

from pathlib import Path

from datetime import datetime



save_path = f"{getcwd()}/raw_data"
client = SRSClient()

routes = {
    Item.CHARACTERS : CHARACTERS,
    Item.PLAYERCARD : PLAYERCARDS,
    Item.FOOD : CONSUMABLES,
    Item.RELIC : RELICS,
    Item.LIGHTCONE : LIGHTCONES,
    Item.BOOK : BOOKS,
    Item.MATERIAL : MATERIALS,    

}

folders = {
    Item.CHARACTERS : 'characters/',
    Item.PLAYERCARD : 'playercards/',
    Item.FOOD : 'foods/',
    Item.RELIC : 'relics/',
    Item.LIGHTCONE : 'lightcones/',
    Item.BOOK : 'books/',
    Item.MATERIAL : 'materials/'
}

def create_path(path :str):
    path_ = Path(f'{save_path}/{path}')
    if not exists(f'{save_path}/{path}'):
        path_.mkdir(parents=True)
    

def correct_route(url : str):
   return url.replace('/','s/',1)

def convert(seconds: int | float):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)

START_TIME = datetime.now()

language = Language.EN
'''
iterate over all languages to get data in all languages
'''



#for language in Languages:  
'''
iterate over all languages to get data in all languages
'''

for type in Item: 
    '''

    Iterate over all Item to get all data
    '''
    entries = client.get_all_items(None, language) # this gets all items that exist in search database of starrailstation.com
    
    for entry in entries:
        create_path(f'{language}/{folders[entry.type]}')
        if not exists(f'{save_path}/{language}/{folders[entry.type]}/{entry.id}.json'):

            '''
            fetches data
            '''
            data = client.fetch(language, routes[entry.type], True, entry.id)              
            print(f'[downloading] [Language: {language}]', Item(entry.type).name, entry.name)
            with open(f'{save_path}/{language}/{folders[entry.type]}/{entry.id}.json', 'w') as f:
                dump(data, f, indent=1)


print(f'[downloading] [Language: {language}]', 'ACHIEVEMENTS')   
data = client.fetch(language, ACHIEVEMENTS, None)
with open(f'{save_path}/{language}/achievements.json', 'w') as f:
    dump(data, f, indent=1)


print(f'[downloading] [Language: {language}]', 'SIMULATED UNIVERSE', 'Date', ROUGE_DATE)     

data = client.fetch(language, ROUGES, None)
with open(f'{save_path}/{language}/simulatedUniverse.json', 'w') as f:
    dump(data, f, indent=1)



END_TIME = datetime.now()
print(f' [HSR-DATA] download completed in {convert((END_TIME - START_TIME).total_seconds())}')