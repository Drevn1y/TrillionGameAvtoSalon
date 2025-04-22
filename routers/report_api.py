from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from starlette.staticfiles import StaticFiles
from database.models import Report
from database import get_db
from sqlalchemy.orm import Session
import os
from uuid import uuid4
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime

# Создаем компонент
reports_router = APIRouter(prefix='/reports', tags=['Отчеты'])

# Директория для хранения файлов отчетов
UPLOAD_DIR = "files/reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Указываем директорию с файлами отчетов
reports_router.mount("/reports", StaticFiles(directory="files/reports"), name="reports")


# Получить все отчеты
def get_all_reports_db(db: Session):
    return db.query(Report).all()


@reports_router.get('/all')
async def get_all_reports(db: Session = Depends(get_db)):
    reports = get_all_reports_db(db)
    return reports


# Найти отчет по ID
def get_report_db(report_id: int, db: Session):
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Отчет не найден")
    return report


@reports_router.get('/{report_id}')
async def get_report(report_id: int, db: Session = Depends(get_db)):
    return get_report_db(report_id, db)


# Добавить отчет (загрузить файл)
async def add_report_db(file: UploadFile, branch_id: int, db: Session):
    # Генерируем уникальное имя для файла
    file_name = f"{uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    # Сохраняем файл на сервер
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Создаем запись в базе данных
    new_report = Report(
        branch_id=branch_id,
        report_file=file_path,
        report_date=datetime.now()
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


@reports_router.post('/add')
async def add_report(
        file: UploadFile = File(description="Файл отчета (например, Word)"),
        branch_id: int = Query(description="ID филиала, к которому относится отчет"),
        db: Session = Depends(get_db)
):
    return await add_report_db(file, branch_id, db)


# Удалить отчет
def delete_report_db(report_id: int, db: Session):
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Отчет не найден")

    # Удаляем файл с сервера
    if os.path.exists(report.report_file):
        os.remove(report.report_file)

    db.delete(report)
    db.commit()
    return {"message": "Отчет успешно удален"}


@reports_router.delete('/delete/{report_id}')
async def delete_report(report_id: int, db: Session = Depends(get_db)):
    return delete_report_db(report_id, db)


# Получить все отчеты определенного филиала
def get_reports_by_branch_id_db(branch_id: int, db: Session):
    reports = db.query(Report).filter(Report.branch_id == branch_id).all()
    if not reports:
        raise HTTPException(status_code=404, detail="Отчеты не найдены")
    return reports


@reports_router.get('/branch/{branch_id}')
async def get_reports_by_branch_id(branch_id: int, db: Session = Depends(get_db)):
    return get_reports_by_branch_id_db(branch_id, db)
