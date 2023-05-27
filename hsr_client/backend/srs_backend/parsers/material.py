
from hsr_client.backend.srs_backend import SRSBackend
from hsr_client.datamodels.chara import Character
from hsr_client.datamodels.eidolon import Eidolon
from bs4 import BeautifulSoup

from hsr_client.datamodels.material import Material


def parse_material(mat_id, be: SRSBackend) -> Material:



    # TODO: create the actual material with ID.

    # actually , can just move backend fetch this out of here and put it in srs_backend
    # just let this function parse materail nothing else.

    material = Material(
        name="foo",
        rarity=4,
        description="mat description",
        lore = "some lore",
        source=["somewhere"]
    ) # type: ignore

    return material
