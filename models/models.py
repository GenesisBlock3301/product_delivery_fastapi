from typing import Text
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from .databases import Base
from sqlalchemy_utils.types import ChoiceType


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True, index=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Orders", back_populates="user")

    def __str__(self) -> str:
        return f"{self.username}"


class Orders(Base):
    ORDER_STATUSES = (
        ('PENDING', "pending"),
        ('IN-TRANSIT', "in-transit"),
        ('DELIVERED', "delivered")
    )

    PIZZA_SIZES = (
        ("SMALL", "small"),
        ("MEDIUM", "medium"),
        ("LARGE", "large"),
    )
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUSES), default="PENDING")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users",back_populates='orders')
    def __str__(self) -> str:
        return f"User {self.user_id}"
