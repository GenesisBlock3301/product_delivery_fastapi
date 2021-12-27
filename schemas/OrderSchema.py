from typing import Optional
from pydantic import BaseModel


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = "PENDING"
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "quantity": 5,
            }
        }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = "PENDING"

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "order_status": "PENDING"
            }
        }
