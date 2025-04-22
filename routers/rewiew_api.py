from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database.models import BranchReview, Branch, User
from database import get_db
from routers import BranchReviewCreateUpdate

# Создаем компонент
branch_review_router = APIRouter(prefix='/branch_reviews', tags=['Управление с отзывами филиалов'])

# Получить все отзывы филиалов
def get_branch_review_db(db: Session):
    all_reviews = db.query(BranchReview).all()
    return all_reviews

@branch_review_router.get('/')
async def get_branch_review(db: Session = Depends(get_db)):
    return get_branch_review_db(db)

# Добавить отзыв филиала
def add_rate_db(db: Session, branch_id: int, user_id: int, review_text: str, rating: int):
    # Проверяем, существует ли филиал и пользователь
    branch = db.query(Branch).filter(Branch.branch_id == branch_id).first()
    if not branch:
        raise HTTPException(status_code=404, detail="Филиал не найден")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Создаем новый отзыв
    new_review = BranchReview(
        branch_id=branch_id,
        user_id=user_id,
        review_text=review_text,
        rating=rating,
        review_date=datetime.now()
    )
    db.add(new_review)
    db.commit()
    return {"message": "Отзыв добавлен"}

@branch_review_router.post('/add')
async def add_rate(review_data: BranchReviewCreateUpdate, db: Session = Depends(get_db)):
    result = add_rate_db(
        db=db,
        branch_id=review_data.branch_id,
        user_id=review_data.user_id,
        review_text=review_data.review_text,
        rating=review_data.rating
    )
    return result

# Удалить отзыв
def delete_review_db(db: Session, review_id: int):
    review = db.query(BranchReview).filter(BranchReview.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    db.delete(review)
    db.commit()
    return {"message": "Отзыв удален"}

@branch_review_router.delete('/delete/{review_id}')
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    result = delete_review_db(db, review_id=review_id)
    return result

# Изменить отзыв
def update_review_db(db: Session, review_id: int, review_text: str, rating: int):
    review = db.query(BranchReview).filter(BranchReview.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")

    if review_text:
        review.review_text = review_text
    if rating:
        review.rating = rating

    db.commit()
    return {"message": "Отзыв обновлен"}

@branch_review_router.put('/edit/{review_id}')
async def update_review(review_id: int, review_text: str, rating: int, db: Session = Depends(get_db)):
    result = update_review_db(db, review_id=review_id, review_text=review_text, rating=rating)
    return result

# Найти определенный отзыв
def get_review_by_id_db(db: Session, review_id: int):
    review = db.query(BranchReview).filter(BranchReview.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    return review

@branch_review_router.get('rate/{review_id}')
async def get_review_by_id(review_id: int, db: Session = Depends(get_db)):
    return get_review_by_id_db(db, review_id=review_id)
