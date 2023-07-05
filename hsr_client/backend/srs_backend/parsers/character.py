from typing import Dict
from hsr_client.backend.srs_backend import SRSBackend
from hsr_client.backend.srs_backend.parsers.eidolon import parse_eidolon
from hsr_client.backend.srs_backend.parsers.material import parse_material
from hsr_client.backend.srs_backend.parsers.trace import parse_non_skill_traces
from hsr_client.datamodels.chara import Character
from hsr_client.datamodels.element import Element
from hsr_client.datamodels.lightcone import MaterialCount, Lightcone
from hsr_client.datamodels.material import Material
from hsr_client.paths import Path
from bs4 import BeautifulSoup


def parse_character(character_raw, srs_be: SRSBackend) -> Character:
    # name
    c_name = character_raw["name"]
    # rarity
    c_rarity = character_raw["rarity"]
    # description
    c_description = BeautifulSoup(character_raw["descHash"], features="lxml").get_text()

    # element
    c_element = None
    raw_element = character_raw["damageType"]["name"]
    if raw_element == "Ice":
        c_element = Element.ICE
    else:
        raise Exception(f"failed to parse lightcone, raw_path unknown: ${raw_path}")

    # path
    c_path = None
    raw_path = character_raw["baseType"]["name"]
    if raw_path == "The Hunt":
        c_path = Path.HUNT
    elif raw_path == "Harmony":
        c_path = Path.HARMONY
    elif raw_path == "Destruction":
        c_path = Path.DESTRUCTION
    elif raw_path == "Erudition":
        c_path = Path.ERUDITION
    elif raw_path == "Nihility":
        c_path = Path.NIHILITY
    elif raw_path == "Preservation":
        c_path = Path.PRESERVATION
    elif raw_path == "Abundance":
        c_path = Path.ABUNDANCE
    else:
        raise Exception(f"failed to parse lightcone, raw_path unknown: ${raw_path}")


    # eidolons
    c_eidolons = []
    # resonance aka rank. aka eidolon number
    for resonance_data in character_raw["ranks"]:
        c_eidolons.append(parse_eidolon(resonance_data))

   
    # traces.
    c_traces = []
    parse_non_skill_traces(character_raw['skillTreePoints'], c_traces)

    # ascension_mats



 

    # ascension_mats={
    #     20: [
    #         MaterialCount(
    #             material=Material(name="foo1", description="bar1"), count=1
    #         ),
    #         MaterialCount(
    #             material=Material(name="foo2", description="bar2"), count=2
    #         ),
    #     ],
    #     30: [
    #         MaterialCount(
    #             material=Material(name="foo3", description="bar3"), count=3
    #         ),
    #     ],
    # },


    character = Character(
        name=c_name,
        rarity=c_rarity,
        description=c_description,
        path=c_path,
        eidolons=c_eidolons,
        traces=c_traces,
        element=c_element,
    )



    # _stats (has to be done after object creation)
    setattr(character, "_chara_levelData", character_raw["levelData"])
    setattr(character, '_chara_skills', character_raw['skills'])
    setattr(character, '_backend', srs_be)
  
    return character