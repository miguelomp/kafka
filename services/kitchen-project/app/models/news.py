from datetime import datetime

from pydantic import BaseModel

from .orders import Order


class News(BaseModel):
    order: Order
    message: str
    date: datetime = datetime.now()

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp()
        }
