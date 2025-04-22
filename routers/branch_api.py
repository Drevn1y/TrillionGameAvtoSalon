from http.client import HTTPException

from fastapi import APIRouter
from database.models import Branch
from database import get_db
from routers import BranchCreateUpdate

# Создаем компонент
branch_router = APIRouter(prefix='/branches', tags=['Управление с филиалами'])


# Получить все филиалы
def get_all_branches_db():
    db = next(get_db())
    all_branches = db.query(Branch).all()
    return all_branches

@branch_router.get('/all')
async def get_all_branches():
    return get_all_branches_db()

# Получить определенный филиал
def get_branch_by_id(branch_id: int):
    db = next(get_db())
    branch = db.query(Branch).filter(Branch.branch_id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Филиал не найден")
    return branch

@branch_router.get('/branch/{branch_id}')
async def get_branch_by_id_route(branch_id: int):
    return get_branch_by_id(branch_id=branch_id)

# Добавить филиал
def add_new_branch_db(branch_name: str, address: str, open_time: str, closed_time: str, phone_number: str):
    db = next(get_db())
    new_branch = Branch(
        branch_name=branch_name,
        address=address,
        open_time=open_time,
        closed_time=closed_time,
        phone_number=phone_number
    )
    db.add(new_branch)
    db.commit()
    return {"message": "Филиал добавлен"}

@branch_router.post('/add-branch')
async def add_new_branch(branch_data: BranchCreateUpdate):
    result = add_new_branch_db(
        branch_name=branch_data.branch_name,
        address=branch_data.address,
        open_time=branch_data.open_time,
        closed_time=branch_data.closed_time,
        phone_number=branch_data.phone_number
    )
    return result

# Удалить филиал
def delete_branch_db(branch_id: int):
    db = next(get_db())
    branch = db.query(Branch).filter(Branch.branch_id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Филиал не найден")
    db.delete(branch)
    db.commit()
    return {"message": "Филиал удален"}

@branch_router.delete('/delete/{branch_id}')
async def delete_branch(branch_id: int):
    result = delete_branch_db(branch_id=branch_id)
    return result

# Изменить инфо о филиале
def update_branch_db(branch_id: int, branch_name: str, address: str, open_time: str, closed_time: str, phone_number: str):
    db = next(get_db())
    branch = db.query(Branch).filter(Branch.branch_id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Филиал не найден")

    if branch_name:
        branch.branch_name = branch_name
    if address:
        branch.address = address
    if open_time:
        branch.open_time = open_time
    if closed_time:
        branch.closed_time = closed_time
    if phone_number:
        branch.phone_number = phone_number

    db.commit()
    return {"message": "Информация о филиале изменена"}

@branch_router.put('/edit-branch/{branch_id}')
async def update_branch(branch_id: int, branch_data: BranchCreateUpdate):
    result = update_branch_db(
        branch_id=branch_id,
        branch_name=branch_data.branch_name,
        address=branch_data.address,
        open_time=branch_data.open_time,
        closed_time=branch_data.closed_time,
        phone_number=branch_data.phone_number
    )
    return result