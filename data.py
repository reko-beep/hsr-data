import requests
from json import load, dump, loads, dumps
from os import mkdir, getcwd, listdir
from os.path import exists, isfile, isdir
from time import sleep
import ast
from PIL import Image
import re
from io import BytesIO

path = getcwd()




def fetch_all_ids():

    '''
    fetches all ids from starrailstation.com
    and updates in json files

    ------------
    creates:
    ------------

    'first_ids.json'
    'second_ids.json'
    
    '''
    data = {
        'first_ids.json': {},
        'second_ids.json': {}
    }
    LINK = 'https://starrailstation.com/static/js/main.1a526542.js'

    with requests.get(LINK) as r:
        if r.status_code <= 300:

            json_raw = r.text     

            second_ids = json_raw[json_raw.find('s.u='):]        
            second_ids = second_ids[second_ids.find('{'):]
            second_ids = second_ids[:second_ids.find('}')+1]
            second_ids = second_ids[second_ids.find('+{')+1:]
            second_ids = ast.literal_eval(second_ids)

            first_ids = json_raw[json_raw.find('52280:function(e,n,s){var o={')+len('52280:function(e,n,s){var o='):]
            first_ids = first_ids[:first_ids.find('}')+1]
            first_ids = ast.literal_eval(first_ids)


            data['first_ids.json'] = first_ids
            data['second_ids.json'] = second_ids


    for d in data:
        
        prev_data = {}
        if exists(d):
            with open(d, 'r') as f:
                prev_data = load(f)
        
        if len(list(set(data[d].keys()).difference(prev_data.keys()))) != 0:
            print('[hsr-data]: new data found for',d)
            with open(d, 'w') as f:
                dump(data[d], f, indent=1)


def beautify_first_ids(language: str):
    '''

    beautify first ids in a seperate json file to be used by script 

    

    ------------
    requirements:
    ------------

    language: es, en, vi, cn, de ,fr, id, jp, kr

    ------------
    creates:
    ------------

    b_first_ids.json
    '''
    if exists('first_ids.json'):

        with open('first_ids.json', 'r') as f:
            data = load(f)

        pass_langs_keys =  ["bannedDetailAvatars.json","bannedLoreAvatars.json", "warpInfo.json"]
        fixed = {}
        for k in data:
            if k.split('/')[1] not in pass_langs_keys:                       
                if k.split('/')[1] == language:                                   
                    main_key = k.split('/')[2]
                    if main_key not in fixed:
                            fixed[main_key] = {}
                    if len(k.split("/")) > 3:
                        sub_key = k.split('/')[3]
                        fixed[main_key][sub_key] = int(data[k][0])
                    else:
                        fixed[main_key] = int(data[k][0])
              

        with open('b_first_ids.json', 'w') as f:
            dump(fixed, f, indent=1)
    
    else:

        raise Exception('[hsr-data] error: run fetch_all_ids first.')

def create_links():

    '''
    creates links from beautified first ids and second ids

    ------------
    requirements:
    ------------

    b_first_ids.json
    second_ids.json

    ------------
    creates:
    ------------
    links.json


    '''
    
    if not exists('b_first_ids.json'):      

        raise Exception('[hsr-data] error: file not found b_first_ids.json, run beautify_first_ids first')
    
    if not exists('first_ids.json') or not exists('second_ids.json'):      

        raise Exception('[hsr-data] error: file not found first_ids.json, run fetch_all_ids first')
    


    with open('b_first_ids.json', 'r') as f:
        obj_ids = load(f)
    
    with open('second_ids.json', 'r') as f:
        tw_ids = load(f)
        
    urls = {} 
    for k in obj_ids:
        if isinstance(obj_ids[k], dict):
            urls[k] = {}
            for id in obj_ids[k]:
                if str(obj_ids[k][id]) in tw_ids:
                    urls[k][id] = f'https://starrailstation.com/static/js/{obj_ids[k][id]}.{tw_ids[str(obj_ids[k][id])]}.chunk.js'
        else:
            urls[k] =f'https://starrailstation.com/static/js/{obj_ids[k]}.{tw_ids[str(obj_ids[k])]}.chunk.js'
    
    with open("links.json", 'w') as f:
        dump(urls, f, indent=1)

def fetch_data():
    '''
    fetches all data in relevant directories

    ------------
    requirements:
    ------------

    links.json

    ------------
    creates:
    ------------
    json files in relevant directories
    
    '''
    with open("links.json", 'r') as f:        
        links = load(f)
    
    for link in links:
        if exists(path+f"/{link.replace('.json', '', 1)}") is False:
            mkdir(path+f"/{link.replace('.json', '', 1)}")
            
        if not isinstance(links[link], dict):
            if not exists(path+f"/{link.replace('.json', '', 1)}/main.json"):
                with requests.get(links[link]) as f:
                    f.encoding = 'utf-8'
                    text_ = f.text
                    text = text_[text_.find("JSON.parse(")+len("JSON.parse("): ]
                    text = text[:text.find(")}}]);")]    
                    print('[hsr-data]: downloading ',links[link])                    
                    data = ast.literal_eval(text)
                    data = loads(data)
                    with open(path+f"/{link.replace('.json', '', 1)}/main.json", 'w') as r:
                        dump(data, r, indent=1)
                sleep(2)
            else:                
                print('[hsr-data]: ',links[link], ' already exists!') 
        else:
            for sub_link in links[link]:
                if not exists(path+f"/{link.replace('.json', '', 1)}/{sub_link}"):
                    
                    with requests.get(links[link][sub_link]) as f:
                        print('[hsr-data]: downloading ',links[link][sub_link])  
                        f.encoding = 'utf-8'
                        text_ = f.text
                        text = text_[text_.find("JSON.parse(")+len("JSON.parse("): ]
                        text = text[:text.find(")}}]);")]                        
                        data = ast.literal_eval(text)
                        data = loads(data)
                    
                        with open(path+f"/{link.replace('.json', '', 1)}/{sub_link}", 'w') as r:
                            dump(data, r, indent=1)
                    sleep(2)
                else:
                    print('[hsr-data]: ',links[link][sub_link], ' already exists!') 
                
def get_image(assetid: str, category: str = '', name: str = ''):
    '''
    downloads image in categoary

    ---------
    requirements
    --------
    json files in folders
     -assetid
        image assetid
     -category
        directory name
     -name
        image file name

    ----
    creates
    ----

     image file
    '''
    if not exists (path+"/images/"):
        mkdir(path+"/images/")
    if not exists(path+f'/images/{category}/'):
        mkdir(path+f'/images/{category}/')
    
    name = name.lower().replace(' ','_',99).replace("<br>",'',99)
    print('[hsr-data]: downloading image for',name)
    url =  f'https://starrailstation.com/assets/{assetid}.webp'
    if not exists(path+f'/images/{category}/{name}.png'):
        with requests.get(url) as f:
            c = BytesIO(f.content)
            img = Image.open(c, mode='r').convert("RGBA")
            if exists(path+f'/{category}'):
                img.save(path+f'/images/{category}/{name}.png')
            else:
                img.save(path+f'/images/{name}.png')
    else:
        print('[hsr-data]: image ',f'{name}.png', ' already exists in ', path+f'/images/{category}/')


def detect_hash(st_: str):
    
    pattern = re.compile(r"^[a-f0-9]{32}")
    return re.match(pattern, "e8e459ad283c3df43713b2d13203b3dc8c636150d0c536f38e2ad62bd72b6e83")

def get_image_props(filename: str, dict: dict):

    '''
    returns a dicts having image props from a json file
    and data

    ------------
    requirements:
    ------------

     - fetched data    
        json files in relevant directories

    ------------
    creates | returns
    ------------
    
        dictionary : {propKey : propValue}
    '''
    
    r = {}
    nameProps = ['name', 'title']
    imagesProp = ["iconPath", "bgPath", "figPath", "fgPath", "artPath", "miniIconPath", "splashIconPath", "altIconPath"]
    
    keys = set(list(dict.keys())).intersection(imagesProp)
    title = list(set(list(dict.keys())).intersection(nameProps))
    for k in keys:
        if dict[k] != "":
            r[f"{filename}-{k}"] = dict[k]
    return r
        
        

def download_all_images(dir: str = ''):
    '''
    downloads all images

    ------------
    requirements:
    ------------

     - dir [optional]
        category : any folder name

    ------------
    creates | returns
    ------------
    
        images in images folder
    '''
    dirs = [d for d in listdir(getcwd()) if isdir(d)]
    if dir  == '':
        for dir in dirs:
            files = [f"{getcwd()}/{dir}/{f}" for f in listdir(getcwd()+"/"+dir) if isfile(getcwd()+"/"+dir+"/"+f) and 'json' in f]
            for f in files:
                with open(f, 'r') as f_:
                    data = load(f_)
                filename = f.split('/')[-1].replace('.json','',1)
                imgs = get_image_props(filename, data)
                for n in imgs:
                    get_image(imgs[n], dir, f"{filename}-{n}")
    else:
        files = [f"{getcwd()}/{dir}/{f}" for f in listdir(getcwd()+"/"+dir) if isfile(getcwd()+"/"+dir+"/"+f) and 'json' in f]  
        for f in files:
            with open(f, 'r') as f_:
                data = load(f_)
            filename = str(f).split('/')[-1].replace('.json','',1)
            print('[hsr-data]: finding images in ',filename)
            imgs = get_image_props(filename, data)
           
            for n in imgs:
                get_image(imgs[n], dir, f"{filename}-{n}")
     
'''


------------
REMOVE QUOTATION MARKS
-----------

fetch_all_ids()
beautify_first_ids()
create_links()
fetch_data()
download_all_images()


'''


fetch_all_ids()
beautify_first_ids('en')
create_links()
fetch_data()
download_all_images()