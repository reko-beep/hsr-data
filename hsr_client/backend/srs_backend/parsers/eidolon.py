from hsr_client.datamodels.chara import Character
from hsr_client.datamodels.eidolon import Eidolon
from bs4 import BeautifulSoup


def parse_eidolon(raw_data) -> Character:
    # name
    e_name = raw_data["name"]
    # resonance
    e_resonance = raw_data["id"]

    # description
    description_template = BeautifulSoup(
        raw_data["descHash"], features="lxml"
    ).get_text()
    template_params = raw_data["params"]


    for slot_no, template_param in enumerate(template_params, start=1):
        replace_text = f"#{slot_no}[i]"
        description_template = description_template.replace(replace_text, str(template_param))

    e_description = description_template

    eidolon = Eidolon(
        name=e_name,
        resonance=e_resonance,
        description=e_description
    )

    return eidolon
