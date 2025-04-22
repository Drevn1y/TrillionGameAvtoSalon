from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.models import Supplier
from database import get_db

# Создаем компонент для поставщиков
suppliers_router = APIRouter(prefix='/suppliers', tags=['Поставщики'])

# Получить всех поставщиков
def get_all_suppliers_db(db: Session):
    return db.query(Supplier).all()

@suppliers_router.get('/all')
async def get_all_suppliers(db: Session = Depends(get_db)):
    suppliers = get_all_suppliers_db(db)
    return suppliers

# Найти поставщика по ID
def get_supplier_db(supplier_id: int, db: Session):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Поставщик не найден")
    return supplier

@suppliers_router.get('/{supplier_id}')
async def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return get_supplier_db(supplier_id, db)

# Добавить поставщика
def add_supplier_db(supplier_company: str, supplier_phone_number: str, supplier_email: str, supplier_address: str, db: Session):
    new_supplier = Supplier(
        supplier_company=supplier_company,
        supplier_phone_number=supplier_phone_number,
        supplier_email=supplier_email,
        supplier_address=supplier_address
    )
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

@suppliers_router.post('/add')
async def add_supplier(
    supplier_company: str = Query(description="Название компании поставщика"),
    supplier_phone_number: str = Query(description="Телефонный номер поставщика"),
    supplier_email: str = Query(description="Электронная почта поставщика", default=None),
    supplier_address: str = Query(description="Адрес поставщика"),
    db: Session = Depends(get_db)
):
    return add_supplier_db(supplier_company, supplier_phone_number, supplier_email, supplier_address, db)

# Удалить поставщика
def delete_supplier_db(supplier_id: int, db: Session):
    supplier = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Поставщик не найден")

    db.delete(supplier)
    db.commit()
    return {"message": "Поставщик успешно удален"}

@suppliers_router.delete('/delete/{supplier_id}')
async def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return delete_supplier_db(supplier_id, db)
