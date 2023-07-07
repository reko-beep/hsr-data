from data_query.character_data import Character
from data_query.lightcones_data import LightCone


def hsr_character(name: str):
    char = Character(name)
    print(char.json_data())
    print(char.name())
    print(char.rarity())
    print(char.damage_type())
    print(char.path())
    print(char.stat_data_onlevel(60))
    for stat in char.stat_data_max():
        print(stat)
    print(char.stat_at_max())
    print(char.skills())
    for trace in char.trace():
        print(trace)
    for const in char.constellation():
        print(const)


def hsr_lightcone(name_id: int):
    lc = LightCone(name_id)
    print(lc.json_data())
    print(lc.name())
    print(lc.rarity())
    print(lc.level_data())
    print(lc.level_data_onlevel(60))
    print(lc.skill_data())
    print(lc.skill_data_onlevel(4))
    print(lc.skill_descHash(4))


hsr_character("arlan")
print()
hsr_lightcone(20000)
