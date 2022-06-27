from enum import Enum, auto
from random import randint
from typing import List

from pydantic import BaseModel


class Food(Enum):
    PIZZA = auto()
    HAMBURGER = auto()
    FRIES = auto()
    COKE = auto()
    PASTA = auto()

class Status(Enum):
    ORDERED = auto()
    IS_COOKING = auto()
    IS_READY = auto()
    DELIVERED = auto()

class Order(BaseModel):
    uid: int = randint(10**2, 10**5)
    client: int
    foods: List[Food]
    status: Status = Status.DELIVERED
