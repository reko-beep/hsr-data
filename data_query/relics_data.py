import json
import re
import os
from data_query.shared_data.shared_var import readable_descHash

class Relic:
    def __init__(self, relic_id: int):
        with open(f"raw_data/en/relics/{relic_id}.json") as file:
            self.content: dict = json.loads(file.read())


    def name(self):
        return self.content.get("name")

    def set_bonus(self):
        skill_data: list[dict] = self.content.get("skills")
        for data in skill_data:
            desc: str = data.get("desc")
            params: list[float] = data.get("params")
            set_num: int = data.get("useNum")
            output = "relic"
            yield readable_descHash(self.name(), params, desc, set_num, output)

    def pieces_effect(self):
        pieces_data: dict[dict] = self.content.get("pieces")
        return pieces_data

if __name__ == "__main__":
    # for filename in os.listdir("raw_data/en/relics"):
    #     if ".json" in filename:
    #         id = filename.replace(".json", "")
    #         relic = Relic(id)
    #         for data in relic.set_bonus():
    #             print(data)
    relic = Relic(101)
    print(relic.pieces_effect().get("1"))