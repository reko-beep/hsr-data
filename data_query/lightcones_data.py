import json
import os
from typing import Dict, List
from data_query.shared_data.shared_var import SharedVar


class LightCone:
    def __init__(self, name: str = None) -> None:
        with open(f"raw_data/en/lightcones/{name}.json") as file:
            self.content: Dict = json.loads(file.read())

    def json_data(self) -> List[str]:
        return [data for data in self.content.keys()]

    def name(self) -> str:
        return self.content["name"]

    def rarity(self) -> int:
        return self.content["rarity"]

    def level_data(self) -> List[Dict]:
        return self.content["levelData"]

    def level_data_onlevel(self, level: int = 80) -> Dict | str:
        level_list: List[int] = SharedVar.level()
        levelData: List[Dict] = self.level_data()
        if level in level_list:
            for data in levelData:
                if data["maxLevel"] == level:
                    return data

        else:
            return QueryError.leveldata_outofrange()

    def skill(self):
        skills_data = self.content["skill"]
        return skills_data


lc = LightCone("20000")
print(lc.name())
