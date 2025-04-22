from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import Manager, Branch
from database import get_db
from routers import ManagerCreateUpdate

# Создаем компонент
manager_router = APIRouter(prefix='/managers', tags=['Управление менеджерами'])


# Получить всех менеджеров
def get_all_managers_db(db: Session):
    return db.query(Manager).all()

@manager_router.get('/')
async def get_all_managers(db: Session = Depends(get_db)):
    return get_all_managers_db(db)

# Получить менеджера по ID
def get_manager_by_id_db(db: Session, manager_id: int):
    manager = db.query(Manager).filter(Manager.manager_id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Менеджер не найден")
    return manager

@manager_router.get('/{manager_id}')
async def get_manager_by_id(manager_id: int, db: Session = Depends(get_db)):
    return get_manager_by_id_db(db, manager_id)

# Добавить менеджера
def add_manager_db(db: Session, manager_name: str, manager_lastname: str, manager_phone_number: str, department_branch: int):
    # Проверяем, существует ли филиал
    branch = db.query(Branch).filter(Branch.branch_id == department_branch).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Филиал не найден")

    new_manager = Manager(
        manager_name=manager_name,
        manager_lastname=manager_lastname,
        manager_phone_number=manager_phone_number,
        department_branch=department_branch
    )
    db.add(new_manager)
    db.commit()
    return {"message": "Менеджер добавлен"}

@manager_router.post('/add')
async def add_manager(manager_data: ManagerCreateUpdate, db: Session = Depends(get_db)):
    result = add_manager_db(
        db=db,
        manager_name=manager_data.manager_name,
        manager_lastname=manager_data.manager_lastname,
        manager_phone_number=manager_data.manager_phone_number,
        department_branch=manager_data.department_branch
    )
    return result

# Удалить менеджера
def delete_manager_db(db: Session, manager_id: int):
    manager = db.query(Manager).filter(Manager.manager_id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Менеджер не найден")
    db.delete(manager)
    db.commit()
    return {"message": "Менеджер удален"}

@manager_router.delete('/delete/{manager_id}')
async def delete_manager(manager_id: int, db: Session = Depends(get_db)):
    result = delete_manager_db(db, manager_id)
    return result

# Обновить менеджера
def update_manager_db(db: Session, manager_id: int, manager_name: str, manager_lastname: str, manager_phone_number: str, department_branch: int):
    manager = db.query(Manager).filter(Manager.manager_id == manager_id).first()
    if not manager:
        raise HTTPException(status_code=404, detail="Менеджер не найден")

    if manager_name:
        manager.manager_name = manager_name
    if manager_lastname:
        manager.manager_lastname = manager_lastname
    if manager_phone_number:
        manager.manager_phone_number = manager_phone_number
    if department_branch:
        # Проверяем, существует ли филиал
        branch = db.query(Branch).filter(Branch.branch_id == department_branch).first()
        if not branch:
            raise HTTPException(status_code=404, detail="Филиал не найден")
        manager.department_branch = department_branch

    db.commit()
    return {"message": "Информация о менеджере обновлена"}

@manager_router.put('/edit/{manager_id}')
async def update_manager(manager_id: int, manager_data: ManagerCreateUpdate, db: Session = Depends(get_db)):
    result = update_manager_db(
        db=db,
        manager_id=manager_id,
        manager_name=manager_data.manager_name,
        manager_lastname=manager_data.manager_lastname,
        manager_phone_number=manager_data.manager_phone_number,
        department_branch=manager_data.department_branch
    )
    return result