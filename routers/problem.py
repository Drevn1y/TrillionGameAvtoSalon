from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database.models import Problem, User, Branch
from database import get_db
from routers import ProblemCreateUpdate

# Создаем компонент
problem_router = APIRouter(prefix='/problems', tags=['Управление жалобами'])

# Получить все жалобы
def get_all_problems_db(db: Session):
    return db.query(Problem).all()

@problem_router.get('/')
async def get_all_problems(db: Session = Depends(get_db)):
    return get_all_problems_db(db)

# Получить жалобу по ID
def get_problem_by_id_db(db: Session, problem_id: int):
    problem = db.query(Problem).filter(Problem.problem_id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")
    return problem

@problem_router.get('/{problem_id}')
async def get_problem_by_id(problem_id: int, db: Session = Depends(get_db)):
    return get_problem_by_id_db(db, problem_id)

# Добавить жалобу
def add_problem_db(db: Session, user_id: int, branch_id: int, problem_text: str):
    # Проверяем, существует ли пользователь и филиал
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    branch = db.query(Branch).filter(Branch.branch_id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Филиал не найден")

    new_problem = Problem(
        user_id=user_id,
        branch_id=branch_id,
        problem_text=problem_text,
        problem_date=datetime.now()
    )
    db.add(new_problem)
    db.commit()
    return {"message": "Жалоба добавлена"}

@problem_router.post('/add')
async def add_problem(problem_data: ProblemCreateUpdate, db: Session = Depends(get_db)):
    result = add_problem_db(
        db=db,
        user_id=problem_data.user_id,
        branch_id=problem_data.branch_id,
        problem_text=problem_data.problem_text
    )
    return result

# Удалить жалобу
def delete_problem_db(db: Session, problem_id: int):
    problem = db.query(Problem).filter(Problem.problem_id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")
    db.delete(problem)
    db.commit()
    return {"message": "Жалоба удалена"}

@problem_router.delete('/delete/{problem_id}')
async def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    result = delete_problem_db(db, problem_id)
    return result

# Обновить жалобу
def update_problem_db(db: Session, problem_id: int, problem_text: str):
    problem = db.query(Problem).filter(Problem.problem_id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Жалоба не найдена")

    if problem_text:
        problem.problem_text = problem_text

    db.commit()
    return {"message": "Информация о жалобе обновлена"}

@problem_router.put('/edit/{problem_id}')
async def update_problem(problem_id: int, problem_text: str, db: Session = Depends(get_db)):
    result = update_problem_db(db, problem_id, problem_text)
    return result