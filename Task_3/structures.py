""" File with structures for task #3"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class Column:
    index: str
    sort: int

@dataclass
class OrderBy:
    direction: str
    index: str

@dataclass
class Condition:
    type: str
    value: str

@dataclass
class ColorCondition:
    type: str
    value: str
    color: Optional[str] = ''

@dataclass
class Result:
    columns: list[Column]
    order_by: Optional[OrderBy] = None
    conditions_data: Optional[dict[str,list[Condition]]] = None
    color_conditions: Optional[dict[str,list[ColorCondition]]] = None
    page_size: Optional[str] = None
    row_height: Optional[str] = None
