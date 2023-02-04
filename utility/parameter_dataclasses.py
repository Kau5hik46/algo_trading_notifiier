__author__ = "Lavanya Naresh"
__editors__ = [""]
__created__ = "04-Feb-2023"
__modified__ = "04-Feb-2023"

from pydantic import BaseModel
from typing import Optional

"""
Update position class as required
"""


# TODO: current position class is a dummy class.
class Position(BaseModel):
    x: float
    y: float


class data_basemodel(BaseModel):
    position: Position
    ltp: float
    mtm: float
    todo_actions: str
    addi_notes: Optional[list[str]] | Optional[str]
