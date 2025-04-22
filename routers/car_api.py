from fastapi import APIRouter, UploadFile, File, Depends, Request, HTTPException
from starlette.staticfiles import StaticFiles
from database.models import Car
from database import get_db
from routers import CarValidator
import os
from uuid import uuid4
from fastapi.responses import FileResponse


# Создаем компонент
car_router = APIRouter(prefix='/cars', tags=['Управление с Машинами'])

UPLOAD_DIR = "files/uploads"

# Указываем директорию с изображениями
car_router.mount("/uploads", StaticFiles(directory="files/uploads"), name="uploads")

# Получить все Машины
def get_all_cars_db():
    db = next(get_db())
    all_cars = db.query(Car).all()
    return all_cars


@car_router.get('/all-cars')
async def get_all_cars():
    return get_all_cars_db()


# Путь для отображения фото
@car_router.get("/files/uploads/{file_name}")
async def get_file(file_name: str):
    file_path = f"files/uploads/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")



# Получить определенную машину
def get_exact_car_db(car_id):
    db = next(get_db())

    exact_post = db.query(Car).filter_by(car_id=car_id).first()

    if exact_post:
        return exact_post
    else:
        return 'Такая машина не найдена'


@car_router.get('/get-car')
async def get_exact_car(car_id):
    result = get_exact_car_db(car_id=car_id)

    return result


# Удалить машину
def delete_car_db(car_id):
    db = next(get_db())

    delete_car = db.query(Car).filter_by(car_id=car_id).first()
    if delete_car:
        db.delete(delete_car)
        db.commit()
        return 'Машина успешно удалена!'
    else:
        return 'Машина не найдена!'


# Удалить машину
@car_router.delete('/delete-car')
async def delete_car(car_id):
    result = delete_car_db(car_id=car_id)

    if result:
        return 'Машина удалена успешно!'
    else:
        return 'Машина с такой айди не найдена!'


# Редактирование машины
def edit_car_db(car_id, new_data):
    db = next(get_db())

    edit_car = db.query(Car).filter_by(car_id=car_id).first()

    if edit_car:
        for field, value in new_data.dict().items():
            if value is not None and hasattr(edit_car, field):
                setattr(edit_car, field, value)

        db.commit()
        return f'Машина с ID {car_id} успешно отредактирована'
    else:
        return 'Машина с таким ID не найдена'


# Редактирование машины
@car_router.put('/edit-car/{car_id}')
async def edit_car(car_id: int, data: CarValidator):
    result = edit_car_db(car_id, data)

    return {'message': result}


# Добавить тачку
def add_new_car_db(car_price, car_name, car_company, car_mileage, car_color, car_year, car_photo):
    db = next(get_db())

    result = Car(
        car_price=car_price,
        car_name=car_name,
        car_company=car_company,
        car_mileage=car_mileage,
        car_color=car_color,
        car_year=car_year,
        car_photo=car_photo
    )
    db.add(result)
    db.commit()
    return result.car_id


@car_router.post('/add-new-car')
async def add_new_car(
        car_price: float,
        car_name: str,
        car_company: str,
        car_mileage: int,
        car_color: str,
        car_year: int,
        car_photo: UploadFile = File(None)
):
    photo_path = None

    if car_photo:
        file_ext = car_photo.filename.split(".")[-1]
        file_name = f"{uuid4()}.{file_ext}"
        photo_path = os.path.join(UPLOAD_DIR, file_name)

        with open(photo_path, "wb") as buffer:
            buffer.write(await car_photo.read())

    new_car = add_new_car_db(
        car_price=car_price,
        car_name=car_name,
        car_company=car_company,
        car_mileage=car_mileage,
        car_color=car_color,
        car_year=car_year,
        car_photo=photo_path
    )

    return {'message': 'Успешно добавлен', 'car_id': new_car}