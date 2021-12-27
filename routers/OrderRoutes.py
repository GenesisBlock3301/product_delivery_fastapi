from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status
from models.databases import get_db
from fastapi_jwt_auth.auth_jwt import AuthJWT
from models.models import Orders, Users
from schemas.OrderSchema import OrderModel, OrderStatusModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/orders", tags=['Orders'])


@router.get("/")
async def Greating(Authorize: AuthJWT = Depends()):
    """
    ## A sample doc about greeting.
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.post("/order")
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    ## Placing an order
    This requires the following
    - quantity: integer
    - 
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = db.query(Users).filter(Users.username == current_user).first()
    new_order = Orders(
        quantity=order.quantity
    )
    new_order.user = user
    db.add(new_order)
    db.commit()
    response = {
        "pizza_size": order.pizza_size,
        "quantity": order.quantity,
    }
    return jsonable_encoder(response)


@router.get("/orders")
async def list_all_orders(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = db.query(Users).filter(Users.username == current_user).first()

    if user.is_staff:
        orders = db.query(Orders).all()
        return jsonable_encoder(orders)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not superuser")


@router.get("/orders/{id}")
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = db.query(Users).filter(Users.username == current_user).first()
    if user.is_staff:
        order = db.query(Orders).filter(Orders.id == id).first()
        return jsonable_encoder(order)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User not allowed to carry out request.")


@router.get("/user/orders")
async def get_user_orders(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    user = Authorize.get_jwt_subject()
    current_user = db.query(Users).filter(Users.username == user).first()
    return jsonable_encoder(current_user.orders)


@router.get("/user/order/{id}")
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    subject = Authorize.get_jwt_subject()
    current_user = db.query(Users).filter(Users.username == subject).first()
    orders = current_user.orders

    for order in orders:
        if order.id == id:
            return jsonable_encoder(order)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="No order with such id.")


@router.put("/order/update/{order_id}")
async def update_order(order_id: int, order: OrderModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    update_order = db.query(Orders).filter(Orders.id == order_id).first()
    update_order.quantity = order.quantity
    db.commit()
    response = {
        "quantity": update_order.quantity,
    }
    return jsonable_encoder(response)


@router.patch("/order/status/{order_id}")
async def update_order(order_id: int, order: OrderStatusModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    username = Authorize.get_jwt_subject()
    current_user = db.query(Users).filter(Users.username == username).first()

    if current_user.is_staff:
        update_order = db.query(Orders).filter(Orders.id == order_id).first()
        update_order.order_status = order.order_status
        db.commit()
        return jsonable_encoder(update_order)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not superuser")


@router.delete("/order/{order_id}")
async def delete_order(order_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    order = db.query(Orders).filter(Orders.id == order_id).first()
    db.delete(order)
    db.commit()
    return order
