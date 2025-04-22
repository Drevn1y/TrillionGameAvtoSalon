from database import get_db
from database.models import Invoice
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from datetime import date
from pydantic import BaseModel

invoice_router = APIRouter(prefix='/invoices', tags=['Счета'])

# Модель для валидации запроса
class InvoiceCreate(BaseModel):
    user_id: int
    total_amount: float
    issue_date: date  # Автоматически конвертирует в формат YYYY-MM-DD
    due_date: date
    status: str


# Получить все счета
def get_all_invoices_db() -> list:
    db: Session = next(get_db())
    all_invoices = db.query(Invoice).all()
    return all_invoices

# Получить счет по ID
def get_invoice_by_id_db(invoice_id: int) -> Invoice:
    db: Session = next(get_db())
    invoice = db.query(Invoice).filter_by(invoice_id=invoice_id).first()
    return invoice

# Добавить новый счет
def add_new_invoice_db(user_id: int, total_amount: float, issue_date: str, due_date: str, status: str) -> int:
    db: Session = next(get_db())
    new_invoice = Invoice(
        user_id=user_id,
        total_amount=total_amount,
        issue_date=issue_date,
        due_date=due_date,
        status=status
    )
    db.add(new_invoice)
    db.commit()
    return new_invoice.invoice_id

# Удалить счет по ID
def delete_invoice_db(invoice_id: int) -> bool:
    db: Session = next(get_db())
    invoice = db.query(Invoice).filter_by(invoice_id=invoice_id).first()
    if invoice:
        db.delete(invoice)
        db.commit()
        return True
    return False


# Получить все счета
@invoice_router.get('/all-invoices')
async def get_all_invoices():
    invoices = get_all_invoices_db()
    return invoices

# Получить счет по ID
@invoice_router.get('/get-invoice/{invoice_id}')
async def get_invoice(invoice_id: int):
    invoice = get_invoice_by_id_db(invoice_id)
    if invoice:
        return invoice
    else:
        raise HTTPException(status_code=404, detail="Счет не найден")

# Добавить новый счет
@invoice_router.post('/add-new-invoice')
async def add_new_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    new_invoice = Invoice(
        user_id=invoice.user_id,
        total_amount=invoice.total_amount,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        status=invoice.status
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return {"message": "Счет успешно добавлен", "invoice_id": new_invoice.invoice_id}

# Удалить счет
@invoice_router.delete('/delete-invoice/{invoice_id}')
async def delete_invoice(invoice_id: int):
    result = delete_invoice_db(invoice_id)
    if result:
        return {"message": "Счет успешно удален"}
    else:
        raise HTTPException(status_code=404, detail="Счет не найден")
