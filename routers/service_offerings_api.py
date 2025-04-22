from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.models import ServiceOffering
from database import get_db

# Создаем компонент для сервисных услуг
services_router = APIRouter(prefix='/services', tags=['Сервисные услуги'])

# Получить все сервисные услуги
def get_all_services_db(db: Session):
    return db.query(ServiceOffering).all()

@services_router.get('/all')
async def get_all_services(db: Session = Depends(get_db)):
    services = get_all_services_db(db)
    return services

# Найти сервисную услугу по ID
def get_service_db(service_id: int, db: Session):
    service = db.query(ServiceOffering).filter(ServiceOffering.service_id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Сервисная услуга не найдена")
    return service

@services_router.get('/{service_id}')
async def get_service(service_id: int, db: Session = Depends(get_db)):
    return get_service_db(service_id, db)

# Добавить сервисную услугу
def add_service_db(service_name: str, service_description: str, service_price: float, db: Session):
    new_service = ServiceOffering(
        service_name=service_name,
        service_description=service_description,
        service_price=service_price
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@services_router.post('/add')
async def add_service(
    service_name: str = Query(description="Название услуги"),
    service_description: str = Query(description="Описание услуги"),
    service_price: float = Query(description="Цена услуги"),
    db: Session = Depends(get_db)
):
    return add_service_db(service_name, service_description, service_price, db)

# Удалить сервисную услугу
def delete_service_db(service_id: int, db: Session):
    service = db.query(ServiceOffering).filter(ServiceOffering.service_id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Сервисная услуга не найдена")

    db.delete(service)
    db.commit()
    return {"message": "Сервисная услуга успешно удалена"}

@services_router.delete('/delete/{service_id}')
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    return delete_service_db(service_id, db)
