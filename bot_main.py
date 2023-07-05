import json

folder = 'raw_data/en/characters'

#input("Select character data: ")

with open(f'{folder}/arlan.json') as file:
    f = file.read()
character = json.loads(f)

levelData1 = character['skills'][0]['levelData'][8]
levelData2 = character['skills'][1]['levelData'][14]
levelData3 = character['skills'][2]['levelData'][14]
levelData4 = character['skills'][3]['levelData'][14]


def basicATK():
    print(f"{character['skills'][0]['name']} ({character['skills'][0]['typeDescHash']})")
    print(character['skills'][0]['tagHash'])
    print(f"Level {levelData1['level']}: {int(levelData1['params'][0]*100)}% DMG")
    print()  


def skill():
    print(f"{character['skills'][1]['name']} ({character['skills'][1]['typeDescHash']})")
    print(character['skills'][1]['tagHash'])
    print(f"Level {levelData2['level']}: {int(levelData2['params'][1]*100)}% DMG")
    print()  


def ultimate():
    print(f"{character['skills'][2]['name']} ({character['skills'][2]['typeDescHash']})")
    print(character['skills'][2]['tagHash'])
    print(f"Level {levelData3['level']}: {int(levelData3['params'][0]*100)}% DMG ({int(levelData3['params'][1]*100)}% Splash DMG)")
    print() 


def talent():
    print(f"{character['skills'][3]['name']} ({character['skills'][3]['typeDescHash']})")
    print(character['skills'][0]['tagHash'])
    print(f"Level {levelData4['level']}: {int(levelData4['params'][0]*100)}% DMG")
    print()  


def technique():
    print(f"{character['skills'][5]['name']} ({character['skills'][5]['typeDescHash']})")
    print()  


basicATK()
skill()
ultimate()
talent()
technique()