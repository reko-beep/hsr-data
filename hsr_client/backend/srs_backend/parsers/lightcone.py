from hsr_client.datamodels.lightcone import MaterialCount, Lightcone
from hsr_client.datamodels.material import Material
from hsr_client.paths import Path
from bs4 import BeautifulSoup


def parse_lightcone(data) -> Lightcone:
    # name
    lc_name = data["name"]
    # rarity
    lc_rarity = data["rarity"]
    # description
    lc_description = BeautifulSoup(data["descHash"], features="lxml").get_text()

    # path
    lc_path = None
    raw_path = data["baseType"]["name"]

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
        data["skill"]["descHash"], features="lxml"
    ).get_text()
    simp_template_params = map(lambda si: si["params"], data["skill"]["levelData"])

    for simp_no, template_params in enumerate(simp_template_params, start=1):
        ability_desc = ability_desc_template
        for slot_no, template_param in enumerate(template_params, start=1):
            replace_text = f"#{slot_no}[i]"
            # print("replacing: " + replace_text + " with " + str(template_param) + " in " + ability_desc)
            ability_desc = ability_desc.replace(replace_text, str(template_param))

        lc_ability[simp_no] = ability_desc

    lightcone = Lightcone(
        name=lc_name,
        rarity=lc_rarity,
        description=lc_description,
        path=lc_path,
        ability=lc_ability,
        ascension_mats={
            20: [
                MaterialCount(
                    material=Material(name="foo1", description="bar1"), count=1
                ),
                MaterialCount(
                    material=Material(name="foo2", description="bar2"), count=2
                ),
            ],
            30: [
                MaterialCount(
                    material=Material(name="foo3", description="bar3"), count=3
                ),
            ],
        },
    )

    # _stats (has to be done after object creation)
    setattr(lightcone, "_stats", data["levelData"])

    return lightcone
