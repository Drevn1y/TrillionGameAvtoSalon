from fastapi import APIRouter, UploadFile, File, Depends
from database.models import Bus
from database import get_db
from routers import BusValidator
import os
from uuid import uuid4

UPLOAD_DIR = "files/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Создаем компонент
bus_router = APIRouter(prefix='/buses', tags=['Управление с Автобусами'])

# Получить все автобусы
def get_all_buses_db():
    db = next(get_db())
    all_buses = db.query(Bus).all()
    return all_buses

@bus_router.get('/all-buses')
async def get_all_buses():
    return get_all_buses_db()

# Получить определенный автобус
def get_exact_bus_db(bus_id):
    db = next(get_db())
    exact_bus = db.query(Bus).filter_by(bus_id=bus_id).first()
    if exact_bus:
        return exact_bus
    else:
        return 'Такой автобус не найден'

@bus_router.get('/get-bus')
async def get_exact_bus(bus_id):
    result = get_exact_bus_db(bus_id=bus_id)
    return result

# Удалить автобус
def delete_bus_db(bus_id):
    db = next(get_db())
    delete_bus = db.query(Bus).filter_by(bus_id=bus_id).first()
    if delete_bus:
        db.delete(delete_bus)
        db.commit()
        return 'Автобус успешно удален!'
    else:
        return 'Автобус не найден!'

@bus_router.delete('/delete-bus')
async def delete_bus(bus_id):
    result = delete_bus_db(bus_id=bus_id)
    if result:
        return 'Автобус удален успешно!'
    else:
        return 'Автобус с такой айди не найден!'

# Редактирование автобуса
def edit_bus_db(bus_id, new_data):
    db = next(get_db())
    edit_bus = db.query(Bus).filter_by(bus_id=bus_id).first()
    if edit_bus:
        for field, value in new_data.dict().items():
            if value is not None and hasattr(edit_bus, field):
                setattr(edit_bus, field, value)
        db.commit()
        return f'Автобус с ID {bus_id} успешно отредактирован'
    else:
        return 'Автобус с таким ID не найден'


@bus_router.put('/edit-bus/{bus_id}')
async def edit_bus(bus_id: int, data: BusValidator):
    result = edit_bus_db(bus_id, data)
    return {'message': result}

# Добавить автобус
def add_new_bus_db(bus_price, bus_name, bus_company, bus_mileage, bus_color, bus_year, bus_photo):
    db = next(get_db())

    result = Bus(
        bus_price=bus_price,
        bus_name=bus_name,
        bus_company=bus_company,
        bus_mileage=bus_mileage,
        bus_color=bus_color,
        bus_year=bus_year,
        bus_photo=bus_photo
    )
    db.add(result)
    db.commit()
    return result.bus_id


@bus_router.post('/add-new-bus')
async def add_new_bus(
        bus_price: float,
        bus_name: str,
        bus_company: str,
        bus_mileage: int,
        bus_color: str,
        bus_year: int,
        bus_photo: UploadFile = File(None)
):
    photo_path = None

    if bus_photo:
        file_ext = bus_photo.filename.split(".")[-1]
        file_name = f"{uuid4()}.{file_ext}"
        photo_path = os.path.join(UPLOAD_DIR, file_name)

        with open(photo_path, "wb") as buffer:
            buffer.write(await bus_photo.read())

    new_bus = add_new_bus_db(
        bus_price=bus_price,
        bus_name=bus_name,
        bus_company=bus_company,
        bus_mileage=bus_mileage,
        bus_color=bus_color,
        bus_year=bus_year,
        bus_photo=photo_path
    )

    return {'message': 'Успешно добавлен', 'bus_id': new_bus}