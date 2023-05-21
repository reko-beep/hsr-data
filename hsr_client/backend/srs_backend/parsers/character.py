from hsr_client.backend.srs_backend.parsers.eidolon import parse_eidolon
from hsr_client.backend.srs_backend.parsers.trace import parse_traces
from hsr_client.datamodels.chara import Character
from hsr_client.datamodels.element import Element
from hsr_client.datamodels.lightcone import MaterialCount, Lightcone
from hsr_client.datamodels.material import Material
from hsr_client.paths import Path
from bs4 import BeautifulSoup


def parse_character(raw_data) -> Character:
    # name
    c_name = raw_data["name"]
    # rarity
    c_rarity = raw_data["rarity"]
    # description
    c_description = BeautifulSoup(raw_data["descHash"], features="lxml").get_text()

    # element
    c_element = None
    raw_element = raw_data["damageType"]["name"]
    if raw_element == "Ice":
        c_element = Element.ICE
    else:
        raise Exception(f"failed to parse lightcone, raw_path unknown: ${raw_path}")

    # path
    c_path = None
    raw_path = raw_data["baseType"]["name"]
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
    for resonance_data in raw_data["ranks"]:
        c_eidolons.append(parse_eidolon(resonance_data))

   
    # traces.
    c_traces = []
    parse_traces(raw_data["skillTreePoints"], c_traces)


    character = Character(
        name=c_name,
        rarity=c_rarity,
        description=c_description,
        path=c_path,
        eidolons=c_eidolons,
        traces=c_traces,
        element=c_element
        # ascension_mats={
        #     20: [
        #         AscensionMaterial(
        #             material=Material(name="foo1", description="bar1"), count=1
        #         ),
        #         AscensionMaterial(
        #             material=Material(name="foo2", description="bar2"), count=2
        #         ),
        #     ],
        #     30: [
        #         AscensionMaterial(
        #             material=Material(name="foo3", description="bar3"), count=3
        #         ),
        #     ],
        # },
    )

    # _stats (has to be done after object creation)
    # setattr(lightcone, "_stats", raw_data["levelData"])

    return character
