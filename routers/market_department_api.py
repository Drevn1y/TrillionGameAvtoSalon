from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import MarketDepartment
from database import get_db
from routers import MarketDepartmentCreateUpdate

# Создаем компонент
market_department_router = APIRouter(prefix='/market_departments', tags=['Управление отделом маркетинга'])


# Получить все отделы
def get_all_market_departments_db(db: Session):
    return db.query(MarketDepartment).all()

@market_department_router.get('/')
async def get_all_market_departments(db: Session = Depends(get_db)):
    return get_all_market_departments_db(db)

# Получить отдел по ID
def get_market_department_by_id_db(db: Session, department_id: int):
    department = db.query(MarketDepartment).filter(MarketDepartment.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Отдел не найден")
    return department

@market_department_router.get('/{department_id}')
async def get_market_department_by_id(department_id: int, db: Session = Depends(get_db)):
    return get_market_department_by_id_db(db, department_id)

# Добавить отдел
def add_market_department_db(db: Session, department_name: str, department_lastname: str, department_phone_number: str):
    new_department = MarketDepartment(
        department_name=department_name,
        department_lastname=department_lastname,
        department_phone_number=department_phone_number
    )
    db.add(new_department)
    db.commit()
    return {"message": "Отдел добавлен"}

@market_department_router.post('/add')
async def add_market_department(department_data: MarketDepartmentCreateUpdate, db: Session = Depends(get_db)):
    result = add_market_department_db(
        db=db,
        department_name=department_data.department_name,
        department_lastname=department_data.department_lastname,
        department_phone_number=department_data.department_phone_number
    )
    return result

# Удалить отдел
def delete_market_department_db(db: Session, department_id: int):
    department = db.query(MarketDepartment).filter(MarketDepartment.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Отдел не найден")
    db.delete(department)
    db.commit()
    return {"message": "Отдел удален"}

@market_department_router.delete('/delete/{department_id}')
async def delete_market_department(department_id: int, db: Session = Depends(get_db)):
    result = delete_market_department_db(db, department_id)
    return result


# Обновить отдел
def update_market_department_db(db: Session, department_id: int, department_name: str, department_lastname: str, department_phone_number: str):
    department = db.query(MarketDepartment).filter(MarketDepartment.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Отдел не найден")

    if department_name:
        department.department_name = department_name
    if department_lastname:
        department.department_lastname = department_lastname
    if department_phone_number:
        department.department_phone_number = department_phone_number

    db.commit()
    return {"message": "Информация об отделе обновлена"}

@market_department_router.put('/edit/{department_id}')
async def update_market_department(department_id: int, department_data: MarketDepartmentCreateUpdate, db: Session = Depends(get_db)):
    result = update_market_department_db(
        db=db,
        department_id=department_id,
        department_name=department_data.department_name,
        department_lastname=department_data.department_lastname,
        department_phone_number=department_data.department_phone_number
    )
    return result