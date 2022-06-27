from random import randint
from typing import List

from fastapi import APIRouter, HTTPException

from ..configs import ROUTE_ORDERS
from ..dependencies import send_to_kitchen
from ..models.orders import Food, Order

router = APIRouter(prefix=ROUTE_ORDERS)


fake_orders_db: List[Order] = [
    Order(uid=randint(10**2, 10**5), client=0, foods=[Food.PIZZA, Food.COKE]),
    Order(uid=randint(10**2, 10**5), client=1, foods=[Food.HAMBURGER, Food.HAMBURGER, Food.COKE]),
    Order(uid=randint(10**2, 10**5), client=2, foods=[Food.PASTA, Food.COKE])
]

@router.get("/")
async def read_items():
    return fake_orders_db


@router.post("/send")
async def send_order(orders: List[Order]):
    """
    Send orders to kitchen
    """
    for order in orders:
        await send_to_kitchen(order=order)
    return orders

