from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import CenterDepartment
from database import get_db
from routers import CenterDepartmentCreateUpdate

# Создаем компонент
center_department_router = APIRouter(prefix='/center_departments', tags=['Управление отделом кол-центра'])


# Получить все отделы
def get_all_center_departments_db(db: Session):
    return db.query(CenterDepartment).all()

@center_department_router.get('/')
async def get_all_center_departments(db: Session = Depends(get_db)):
    return get_all_center_departments_db(db)

# Получить отдел по ID
def get_center_department_by_id_db(db: Session, department_id: int):
    department = db.query(CenterDepartment).filter(CenterDepartment.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Отдел не найден")
    return department

@center_department_router.get('/{department_id}')
async def get_center_department_by_id(department_id: int, db: Session = Depends(get_db)):
    return get_center_department_by_id_db(db, department_id)

# Добавить отдел
def add_center_department_db(db: Session, department_name: str, department_lastname: str, department_phone_number: str):
    new_department = CenterDepartment(
        department_name=department_name,
        department_lastname=department_lastname,
        department_phone_number=department_phone_number
    )
    db.add(new_department)
    db.commit()
    return {"message": "Отдел добавлен"}

@center_department_router.post('/add')
async def add_center_department(department_data: CenterDepartmentCreateUpdate, db: Session = Depends(get_db)):
    result = add_center_department_db(
        db=db,
        department_name=department_data.department_name,
        department_lastname=department_data.department_lastname,
        department_phone_number=department_data.department_phone_number
    )
    return result

# Удалить отдел
def delete_center_department_db(db: Session, department_id: int):
    department = db.query(CenterDepartment).filter(CenterDepartment.department_id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Отдел не найден")
    db.delete(department)
    db.commit()
    return {"message": "Отдел удален"}

@center_department_router.delete('/delete/{department_id}')
async def delete_center_department(department_id: int, db: Session = Depends(get_db)):
    result = delete_center_department_db(db, department_id)
    return result

# Обновить отдел
def update_center_department_db(db: Session, department_id: int, department_name: str, department_lastname: str, department_phone_number: str):
    department = db.query(CenterDepartment).filter(CenterDepartment.department_id == department_id).first()
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

@center_department_router.put('/edit/{department_id}')
async def update_center_department(department_id: int, department_data: CenterDepartmentCreateUpdate, db: Session = Depends(get_db)):
    result = update_center_department_db(
        db=db,
        department_id=department_id,
        department_name=department_data.department_name,
        department_lastname=department_data.department_lastname,
        department_phone_number=department_data.department_phone_number
    )
    return result