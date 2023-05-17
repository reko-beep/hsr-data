
from typing import Optional
from pydantic import BaseModel
from . import trace

from enum import Enum





# TODO: decide all the parameters
class Character(BaseModel):
    """Traces possessed by the `Character`"""
    # name of the trace.
    name: str
    traces: list[trace.Trace]



