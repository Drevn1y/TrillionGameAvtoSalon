from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import BlackList
from database import get_db

# Создаем компонент для черного списка клиентов
blacklist_router = APIRouter(prefix='/blacklist', tags=['Черный список клиентов'])

# Получить всех клиентов из черного списка
def get_all_blacklist_db(db: Session):
    return db.query(BlackList).all()

@blacklist_router.get('/all')
async def get_all_blacklist(db: Session = Depends(get_db)):
    blacklist = get_all_blacklist_db(db)
    return blacklist

# Найти клиента в черном списке по ID
def get_blacklist_client_db(block_id: int, db: Session):
    client = db.query(BlackList).filter(BlackList.block_id == block_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден в черном списке")
    return client

@blacklist_router.get('/{block_id}')
async def get_blacklist_client(block_id: int, db: Session = Depends(get_db)):
    return get_blacklist_client_db(block_id, db)

# Добавить клиента в черный список
def add_blacklist_client_db(user_id: int, db: Session):
    new_blacklist_client = BlackList(user_id=user_id)
    db.add(new_blacklist_client)
    db.commit()
    db.refresh(new_blacklist_client)
    return new_blacklist_client

@blacklist_router.post('/add')
async def add_blacklist_client(user_id: int, db: Session = Depends(get_db)):
    return add_blacklist_client_db(user_id, db)

# Удалить клиента из черного списка
def delete_blacklist_client_db(block_id: int, db: Session):
    client = db.query(BlackList).filter(BlackList.block_id == block_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден в черном списке")

    db.delete(client)
    db.commit()
    return {"message": "Клиент успешно удален из черного списка"}

@blacklist_router.delete('/delete/{block_id}')
async def delete_blacklist_client(block_id: int, db: Session = Depends(get_db)):
    return delete_blacklist_client_db(block_id, db)
