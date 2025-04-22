from fastapi import APIRouter, Depends, HTTPException
from database.models import WebSite
from database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

# Создаем компонент
website_router = APIRouter(prefix='/website_requests', tags=['Управление с Заявками от сайта'])


# Модель Pydantic для валидации данных
class WebSiteCreate(BaseModel):
    request_name: str
    request_email: str
    request_phone: str
    request_message: str


class WebSiteResponse(WebSiteCreate):
    request_id: int

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy моделями


# Получить все заявки
def get_all_requests_db(db: Session):
    return db.query(WebSite).all()


@website_router.get('/all', response_model=List[WebSiteResponse])
async def get_all_requests(db: Session = Depends(get_db)):
    return get_all_requests_db(db)


# Получить заявку по ID
def get_request_db(request_id: int, db: Session):
    request = db.query(WebSite).filter(WebSite.request_id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return request


@website_router.get('/id/{request_id}', response_model=WebSiteResponse)
async def get_request(request_id: int, db: Session = Depends(get_db)):
    return get_request_db(request_id, db)


# Добавить заявку
def add_request_db(request: WebSiteCreate, db: Session):
    new_request = WebSite(
        request_name=request.request_name,
        request_email=request.request_email,
        request_phone=request.request_phone,
        request_message=request.request_message
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request


@website_router.post('/add/')
async def add_request(request: WebSiteCreate, db: Session = Depends(get_db)):
    return add_request_db(request, db)


# Удалить заявку
def delete_request_db(request_id: int, db: Session):
    request = db.query(WebSite).filter(WebSite.request_id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    db.delete(request)
    db.commit()
    return {"message": "Заявка успешно удалена"}


@website_router.delete('/del/{request_id}')
async def delete_request(request_id: int, db: Session = Depends(get_db)):
    return delete_request_db(request_id, db)