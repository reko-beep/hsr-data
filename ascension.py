from os import listdir, getcwd
from os.path import isdir, isfile, exists
from json import load, dump
from hsr_client.utils import ImageManipulation as img
from PIL import Image

BASE_CHAR = getcwd()+"/characters/"
BASE_MATERIALS =  getcwd()+"/materials/"
chars = [f for f in listdir(BASE_CHAR) if isfile(BASE_CHAR+f)]
materials = [f for f in listdir(BASE_MATERIALS) if isfile(BASE_MATERIALS+f)]
from io import BytesIO
cards_bg = {
            'card_5': Image.open(f'{getcwd()}/cards/card_5.webp').convert("RGBA"),
            'card_3': Image.open(f'{getcwd()}/cards/card_3.webp').convert("RGBA"),
            'card_4': Image.open(f'{getcwd()}/cards/card_4.webp').convert("RGBA"),
            'card_2': Image.open(f'{getcwd()}/cards/card_2.webp').convert("RGBA"),
            'card_1': Image.open(f'{getcwd()}/cards/card_0.webp').convert("RGBA"),
            'card_0': Image.open(f'{getcwd()}/cards/card_0.webp').convert("RGBA")
        }

for char in chars:
    

    name = char.replace(".json","",1)
    if not exists(f"{getcwd()}/ascension/{name}-ascension.png"):
        with open(BASE_CHAR+char, 'r') as f:
            data = load(f)


        costs_dict = {'levels': {}, 'skills': {}}

        items = data['itemReferences']
        levels = data['levelData']

        for lvl in levels:
            costs = lvl['cost']
            print(costs)
            for c in costs:
                if str(c['id']) not in costs_dict['levels']:
                    costs_dict['levels'][str(c['id'])] = c['count']
                else:
                    costs_dict['levels'][str(c['id'])] += c['count']

        skills = data['skills']

        for skill in skills:
            lvls = skill['levelData']
            for lvl in lvls:
                costs = lvl['cost']
                for c in costs:
                    if str(c['id']) not in costs_dict['skills']:
                        costs_dict['skills'][str(c['id'])] = c['count']
                    else:
                        costs_dict['skills'][str(c['id'])] += c['count']


        costs_dict['items'] = items
        cards = {'levels': [], 'skills': []}
        with open("test.json", 'w') as f:
            dump(costs_dict, f, indent=1)
        for it in ['levels', 'skills']:
            for item_id in costs_dict[it]:
                if item_id in costs_dict['items']:            
            
                    
                        with open(f"{getcwd()}/images/materials/{item_id}-{item_id}-iconpath.png", 'rb') as f:
                            
                            bytes_obj = BytesIO(f.read())
                        print(cards_bg[f"card_{costs_dict['items'][str(item_id)]['rarity']}"])                
                        cards[it].append({
                            'card_bg': cards_bg[f"card_{costs_dict['items'][str(item_id)]['rarity']}"],
                            'txt': costs_dict[it][str(item_id)],
                            'img' : bytes_obj,
                            'title': costs_dict['items'][str(item_id)]['name']
                        })
                

        with open(f"{getcwd()}/images/characters/{name}-{name}-splashiconpath.png", "rb") as f:
            bytes_ = BytesIO(f.read())
        bg_img = Image.open(f"{getcwd()}/images/characters/{name}-{name}-bgpath.png", 'r').convert("RGBA")
        img_ = img.create_image_card(name.title(),bytes_, False ,'Ascension',  0, 0, bg_img)

        max_item = 5
        start_x = img_.size[0] // 2 - 250
        start_y = 250   
        end_x = start_x + (112*5)

        cards_list = cards['levels'] + cards['skills']

        rows = 1
        for c, card in enumerate(cards_list,1):
            count_fix = c
            if c > (rows * max_item):
                rows += 1
                count_fix = (c - ((rows-1) * max_item))
            else:
                if rows > 1:
                    count_fix = c - ((rows-1) * max_item)
                else:
                    count_fix = c 
            
            
            c_img = img.create_card_image(card)
            x = start_x + (122 * (count_fix - 1)) + 30
            y = start_y + (145 * (rows - 1))+ 30
            img_.paste(c_img, (x,y), c_img)

        img_ = img_.crop((0,0, 1600, img_.size[1]))
        img_ = img.add_corners(img_,45)
        img_.show()

        img_.save(f"{getcwd()}/ascension/{name}-ascension.png")
