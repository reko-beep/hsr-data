from main import SRSClient
from constants import Types, Languages
from routes import *
from os import getcwd, mkdir
from os.path import exists

from json import dump
from time import sleep

from pathlib import Path





save_path = getcwd()
client = SRSClient()

routes = {
    Types.CHARACTERS : CHARACTERS,
    Types.PLAYERCARDS : MATERIALS,
    Types.FOODS : CONSUMABLES,
    Types.RELICS : RELICS,
    Types.LIGHTCONES : EQUIPMENT,
    Types.BOOKS : BOOKS,
    Types.MATERIALS : MATERIALS

}

folders = {
    Types.CHARACTERS : 'characters/',
    Types.PLAYERCARDS : 'playercards/',
    Types.FOODS : 'foods/',
    Types.RELICS : 'relics/',
    Types.LIGHTCONES : 'equipment/',
    Types.BOOKS : 'books/',
    Types.MATERIALS : 'materials/'
}

def create_path(path :str):
    path_ = Path(f'{save_path}/{path}')
    if not exists(f'{save_path}/{path}'):
        path_.mkdir(parents=True)
    

def correct_route(url : str):
   return url.replace('/','s/',1)



for language in Languages:  
    '''
    iterate over all languages to get data in all languages
    '''

    for type in Types: 
        '''

        Iterate over all types to get all data
        '''
        entries = client.get_all_items(None, language) # this gets all items that exist in search database of starrailstation.com
        
        for entry in entries:
            create_path(f'{language}/{folders[entry.type]}')
            if not exists(f'{save_path}/{language}/{folders[entry.type]}/{entry.id}.json'):

                '''
                fetches data
                '''
                data = client.fetch(language, routes[entry.type], True, entry.id)              
                print(f'[downloading] [Language: {language}]', Types(entry.type).name, entry.name)
                with open(f'{save_path}/{language}/{folders[entry.type]}/{entry.id}.json', 'w') as f:
                    dump(data, f, indent=1)
                sleep(2)


        

