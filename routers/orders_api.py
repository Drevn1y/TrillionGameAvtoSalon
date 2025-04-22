from fastapi import APIRouter, Depends, HTTPException
from database.models import Order
from database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import List

# Создаем компонент
orders_router = APIRouter(prefix='/orders', tags=['Управление с Заказами'])


# Модель Pydantic для валидации данных
class OrderCreate(BaseModel):
    order_name: str
    order_count: int
    order_price: float
    order_date: datetime


class OrderResponse(OrderCreate):
    order_id: int

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy моделями


# Получить все заказы
def get_all_orders_db(db: Session):
    return db.query(Order).all()


@orders_router.get('/', response_model=List[OrderResponse])
async def get_all_orders(db: Session = Depends(get_db)):
    return get_all_orders_db(db)


# Получить заказ по ID
def get_order_db(order_id: int, db: Session):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


@orders_router.get('/{order_id}', response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    return get_order_db(order_id, db)


# Добавить заказ
def add_order_db(order: OrderCreate, db: Session):
    new_order = Order(
        order_name=order.order_name,
        order_count=order.order_count,
        order_price=order.order_price,
        order_date=order.order_date
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@orders_router.post('/', response_model=OrderResponse)
async def add_order(order: OrderCreate, db: Session = Depends(get_db)):
    return add_order_db(order, db)


# Удалить заказ
def delete_order_db(order_id: int, db: Session):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    db.delete(order)
    db.commit()
    return {"message": "Заказ успешно удален"}


@orders_router.delete('/{order_id}')
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    return delete_order_db(order_id, db)