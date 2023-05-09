# for VS Code intellisense only.
from abc import ABC
from datamodels import trace


class Backend(ABC):
    def fetch_traces(self) -> list[trace.Trace]:
        # some default implementations
        ...

    def fetch_image(self) -> str:
        # some default implementation.
        ...