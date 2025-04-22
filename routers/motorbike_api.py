from fastapi import APIRouter, UploadFile, File, Depends
from database.models import Motorbike
from database import get_db
from routers import MotorbikeValidator
import os
from uuid import uuid4

UPLOAD_DIR = "files/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Создаем компонент
motorbike_router = APIRouter(prefix='/motorbikes', tags=['Управление с Мотоциклами'])

# Получить все мотоциклы
def get_all_motorbikes_db():
    db = next(get_db())
    all_motorbikes = db.query(Motorbike).all()
    return all_motorbikes

@motorbike_router.get('/all-motorbikes')
async def get_all_motorbikes():
    return get_all_motorbikes_db()

# Получить определенный мотоцикл
def get_exact_motorbike_db(bike_id):
    db = next(get_db())
    exact_motorbike = db.query(Motorbike).filter_by(bike_id=bike_id).first()
    if exact_motorbike:
        return exact_motorbike
    else:
        return 'Такой мотоцикл не найден'

@motorbike_router.get('/get-motorbike')
async def get_exact_motorbike(bike_id):
    result = get_exact_motorbike_db(bike_id=bike_id)
    return result

# Удалить мотоцикл
def delete_motorbike_db(bike_id):
    db = next(get_db())
    delete_motorbike = db.query(Motorbike).filter_by(bike_id=bike_id).first()
    if delete_motorbike:
        db.delete(delete_motorbike)
        db.commit()
        return 'Мотоцикл успешно удален!'
    else:
        return 'Мотоцикл не найден!'

@motorbike_router.delete('/delete-motorbike')
async def delete_motorbike(bike_id):
    result = delete_motorbike_db(bike_id=bike_id)
    if result:
        return 'Мотоцикл удален успешно!'
    else:
        return 'Мотоцикл с такой айди не найден!'

# Редактирование мотоцикла
def edit_motorbike_db(bike_id, new_data):
    db = next(get_db())
    edit_motorbike = db.query(Motorbike).filter_by(bike_id=bike_id).first()
    if edit_motorbike:
        for field, value in new_data.dict().items():
            if value is not None and hasattr(edit_motorbike, field):
                setattr(edit_motorbike, field, value)
        db.commit()
        return f'Мотоцикл с ID {bike_id} успешно отредактирован'
    else:
        return 'Мотоцикл с таким ID не найден'

@motorbike_router.put('/edit-motorbike/{bike_id}')
async def edit_motorbike(bike_id: int, data: MotorbikeValidator):
    result = edit_motorbike_db(bike_id, data)
    return {'message': result}

# Добавить мотоцикл
def add_new_motorbike_db(bike_price, bike_name, bike_company, bike_mileage, bike_color, bike_year, bike_photo):
    db = next(get_db())

    result = Motorbike(
        bike_price=bike_price,
        bike_name=bike_name,
        bike_company=bike_company,
        bike_mileage=bike_mileage,
        bike_color=bike_color,
        bike_year=bike_year,
        bike_photo=bike_photo
    )
    db.add(result)
    db.commit()
    return result.bike_id


@motorbike_router.post('/add-new-motorbike')
async def add_new_motorbike(
        bike_price: float,
        bike_name: str,
        bike_company: str,
        bike_mileage: int,
        bike_color: str,
        bike_year: int,
        bike_photo: UploadFile = File(None)
):
    photo_path = None

    if bike_photo:
        file_ext = bike_photo.filename.split(".")[-1]
        file_name = f"{uuid4()}.{file_ext}"
        photo_path = os.path.join(UPLOAD_DIR, file_name)

        with open(photo_path, "wb") as buffer:
            buffer.write(await bike_photo.read())

    new_bike = add_new_motorbike_db(
        bike_price=bike_price,
        bike_name=bike_name,
        bike_company=bike_company,
        bike_mileage=bike_mileage,
        bike_color=bike_color,
        bike_year=bike_year,
        bike_photo=photo_path
    )

    return {'message': 'Успешно добавлен', 'motorbike_id': new_bike}