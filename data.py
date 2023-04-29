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

def create_first_ids():
    with open('first_ids.json', 'r') as f:
        data = load(f)
        
    fixed = {}
    for k in data:
        
        main_key = k.split('/')[2]
        if main_key not in fixed:
                fixed[main_key] = {}
                print(len(k.split("/")) > 3)
        if len(k.split("/")) > 3:
            sub_key = k.split('/')[3]
            fixed[main_key][sub_key] = data[k][0]
        else:
            fixed[main_key] = data[k][0]


    with open('obj_ids.json', 'w') as f:
        dump(fixed, f, indent=1)

def create_links():
    
    with open('obj_ids.json', 'r') as f:
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
                    data = ast.literal_eval(text)
                    data = loads(data)
                    with open(path+f"/{link.replace('.json', '', 1)}/main.json", 'w') as r:
                        dump(data, r, indent=1)
                sleep(2)
        else:
            for sub_link in links[link]:
                if not exists(path+f"/{link.replace('.json', '', 1)}/{sub_link}"):
                    print(link, sub_link)
                    with requests.get(links[link][sub_link]) as f:
                        f.encoding = 'utf-8'
                        text_ = f.text
                        text = text_[text_.find("JSON.parse(")+len("JSON.parse("): ]
                        text = text[:text.find(")}}]);")]                        
                        data = ast.literal_eval(text)
                        data = loads(data)
                    
                        with open(path+f"/{link.replace('.json', '', 1)}/{sub_link}", 'w') as r:
                            dump(data, r, indent=1)
                    sleep(2)
                
def get_image(assetid: str, category: str = '', name: str = ''):
    if not exists (path+"/images/"):
        mkdir(path+"/images/")
    if not exists(path+f'/images/{category}/'):
        mkdir(path+f'/images/{category}/')
    print(name)
    name = name.lower().replace(' ','_',99).replace("<br>",'',99)
    url =  f'https://starrailstation.com/assets/{assetid}.webp'
    if not exists(path+f'/images/{category}/{name}.png'):
        with requests.get(url) as f:
            c = BytesIO(f.content)
            img = Image.open(c, mode='r').convert("RGBA")
            if exists(path+f'/{category}'):
                img.save(path+f'/images/{category}/{name}.png')
            else:
                img.save(path+f'/images/{name}.png')

def detect_hash(st_: str):
    
    pattern = re.compile(r"^[a-f0-9]{32}")
    return re.match(pattern, "e8e459ad283c3df43713b2d13203b3dc8c636150d0c536f38e2ad62bd72b6e83")

def get_image_props(filename: str, dict: dict):
    
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
    dirs = [d for d in listdir(getcwd()) if isdir(d)]
    if dir  == '':
        print(dirs)
        for dir in dirs:
            files = [f"{getcwd()}/{dir}/{f}" for f in listdir(getcwd()+"/"+dir) if isfile(getcwd()+"/"+dir+"/"+f) and 'json' in f]
            print(files)
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
            print(filename)
            imgs = get_image_props(filename, data)
           
            for n in imgs:
                get_image(imgs[n], dir, f"{filename}-{n}")
     
create_first_ids()
create_links()
fetch_data()
download_all_images()