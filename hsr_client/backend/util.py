# for VS Code intellisense only.
from typing import List
from abc import ABC
import hsr_client.datamodels as models


class Backend(ABC):
    def fetch_traces(self) -> List[models.trace.Trace]:
        # some default implementations
        ...

    def fetch_image(self) -> str:
        # some default implementation.
        ...

    def get_character(self, target_name) -> models.chara.Character:
        pass