from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from starlette.staticfiles import StaticFiles
from database.models import Agreement
from database import get_db
from sqlalchemy.orm import Session
import os
from uuid import uuid4
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime

# Создаем компонент для договоров
agreement_router = APIRouter(prefix='/agreements', tags=['Договоры'])

# Директория для хранения файлов договоров
UPLOAD_DIR_AGREEMENTS = "files/agreements"
os.makedirs(UPLOAD_DIR_AGREEMENTS, exist_ok=True)

# Указываем директорию с файлами договоров
agreement_router.mount("/agreements", StaticFiles(directory="files/agreements"), name="agreements")


# Получить все договоры
def get_all_agreements_db(db: Session):
    return db.query(Agreement).all()


@agreement_router.get('/all')
async def get_all_agreements(db: Session = Depends(get_db)):
    agreements = get_all_agreements_db(db)
    return agreements


# Найти договор по ID
def get_agreement_db(agreement_id: int, db: Session):
    agreement = db.query(Agreement).filter(Agreement.agreement_id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Договор не найден")
    return agreement


@agreement_router.get('/{agreement_id}')
async def get_agreement(agreement_id: int, db: Session = Depends(get_db)):
    return get_agreement_db(agreement_id, db)


# Добавить договор (загрузить файл)
async def add_agreement_db(file: UploadFile, branch_id: int, db: Session):
    # Генерируем уникальное имя для файла
    file_name = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR_AGREEMENTS, file_name)

    # Сохраняем файл на сервер
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Создаем запись в базе данных
    new_agreement = Agreement(
        branch_id=branch_id,
        agreement_file=file_path,
        agreement_date=datetime.now()
    )

    db.add(new_agreement)
    db.commit()
    db.refresh(new_agreement)
    return new_agreement


@agreement_router.post('/add')
async def add_agreement(
        file: UploadFile = File(description="Файл договора (например, PDF)"),
        branch_id: int = Query(description="ID филиала, к которому относится договор"),
        db: Session = Depends(get_db)
):
    return await add_agreement_db(file, branch_id, db)


# Удалить договор
def delete_agreement_db(agreement_id: int, db: Session):
    agreement = db.query(Agreement).filter(Agreement.agreement_id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Договор не найден")

    # Удаляем файл с сервера
    if os.path.exists(agreement.agreement_file):
        os.remove(agreement.agreement_file)

    db.delete(agreement)
    db.commit()
    return {"message": "Договор успешно удален"}


@agreement_router.delete('/delete/{agreement_id}')
async def delete_agreement(agreement_id: int, db: Session = Depends(get_db)):
    return delete_agreement_db(agreement_id, db)


# Получить все договоры определенного филиала
def get_agreements_by_branch_id_db(branch_id: int, db: Session):
    agreements = db.query(Agreement).filter(Agreement.branch_id == branch_id).all()
    if not agreements:
        raise HTTPException(status_code=404, detail="Договоры не найдены")
    return agreements


@agreement_router.get('/branch/{branch_id}')
async def get_agreements_by_branch_id(branch_id: int, db: Session = Depends(get_db)):
    return get_agreements_by_branch_id_db(branch_id, db)
