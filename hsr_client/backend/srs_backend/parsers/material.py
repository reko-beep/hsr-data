
from bs4 import BeautifulSoup
from ....constants import MaterialTypes
from hsr_client.datamodels.material import Material

from hsr_client.backend.srs_backend import SRSBackend

def parse_material(raw_data, be: SRSBackend) -> Material:


    print(raw_data)


    mtrl_name = raw_data['embeddedItem']['name']
    mtrl_desc = BeautifulSoup(raw_data['embeddedItem']['desc'], features='lxml').get_text()
    mtrl_lore = BeautifulSoup(raw_data['embeddedItem']['lore'], features='lxml').get_text()
    mrtl_source= raw_data['embeddedItem']['comeFrom']
    mtrl_type = MaterialTypes(raw_data['embeddedItem']['purposeId'])

    mtrl_rarity = raw_data['embeddedItem']['rarity']


    # TODO: create the actual material with ID.

    # actually , can just move backend fetch this out of here and put it in srs_backend
    # just let this function parse materail nothing else.

    material = Material(
        name=mtrl_name,
        rarity=mtrl_rarity,
        description=mtrl_desc,
        lore = mtrl_lore,
        type=mtrl_type,
        source=mrtl_source
    )

    return material

