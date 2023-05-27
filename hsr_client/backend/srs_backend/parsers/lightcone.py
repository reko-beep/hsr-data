from hsr_client.datamodels.lightcone import MaterialCount, Lightcone
from hsr_client.datamodels.material import Material
from hsr_client.datamodels.searchItem import SearchItem
from hsr_client.constants import Item

from hsr_client.paths import Path
from hsr_client.constants import MaterialTypes
from hsr_client.backend.srs_backend import SRSBackend

from bs4 import BeautifulSoup


def parse_lightcone(raw_data, be: SRSBackend) -> Lightcone:
    # name
    lc_name = raw_data["name"]
    # rarity
    lc_rarity = raw_data["rarity"]
    # description
    lc_description = BeautifulSoup(raw_data["descHash"], features="lxml").get_text()

    # path
    lc_path = None
    raw_path = raw_data["baseType"]["name"]

    if raw_path == "The Hunt":
        lc_path = Path.HUNT

    elif raw_path == "Harmony":
        lc_path = Path.HARMONY
    elif raw_path == "Destruction":
        lc_path = Path.DESTRUCTION
    elif raw_path == "Erudition":
        lc_path = Path.ERUDITION
    elif raw_path == "Nihility":
        lc_path = Path.NIHILITY
    elif raw_path == "Preservation":
        lc_path = Path.PRESERVATION
    elif raw_path == "Abundance":
        lc_path = Path.ABUNDANCE
    else:
        raise Exception(f"failed to parse lightcone, raw_path unknown: ${raw_path}")

    # ability
    lc_ability = {}
    ability_desc_template = BeautifulSoup(
        raw_data["skill"]["descHash"], features="lxml"
    ).get_text()
    simp_template_params = map(lambda si: si["params"], raw_data["skill"]["levelData"])

    for simp_no, template_params_per_simp in enumerate(simp_template_params, start=1):
        ability_desc = ability_desc_template
        for slot_no, template_param in enumerate(template_params_per_simp, start=1):
            replace_text = f"#{slot_no}[i]"
            # print("replacing: " + replace_text + " with " + str(template_param) + " in " + ability_desc)
            ability_desc = ability_desc.replace(replace_text, str(template_param))

        lc_ability[simp_no] = ability_desc



    # ascension mats
    ascension_mats = []

    for lvl in raw_data['levelData']:
        __lvl = lvl['maxLevel']
        __mtrls = list()
        if 'cost' in lvl:
            for mtrl in lvl['cost']:
                '''
                create an dummy SearchItem just for fetching with ID param and Type            
                '''
                
                __mtrlobj = be.resolve_material(SearchItem(id=int(mtrl['id']), type=Item.MATERIAL, url='', iconPath='', rarity=0, name=''))
                __mtrls.append(MaterialCount(material=__mtrlobj, count=mtrl['count']))
        ascension_mats.append((__lvl, __mtrls))



    # prepare actual lightcone.
    lightcone = Lightcone(
        name=lc_name,
        rarity=lc_rarity,
        description=lc_description,
        path=lc_path,
        ability=lc_ability,
        ascension_mats=dict(ascension_mats),
    )

    # _stats (has to be done after object creation)
    setattr(lightcone, "_stats", raw_data["levelData"])

    return lightcone
