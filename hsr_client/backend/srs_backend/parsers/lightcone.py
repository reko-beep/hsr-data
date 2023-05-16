from hsr_client.datamodels.lightcone import Lightcone
from hsr_client.paths import Path

def parse_lightcone(data) -> Lightcone:
    
    # extract rquired data

    # lightcone.name
    lc_name = data["name"]
    lc_rarity = data["rarity"]
    lc_description = data["descHash"]
    
    lc_path = None
    raw_path = data["baseType"]["name"]
    if raw_path == "The Hunt":
        lc_path = Path.Hunt

    # build and return light cone.