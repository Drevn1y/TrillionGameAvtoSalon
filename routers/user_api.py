from fastapi import APIRouter
from database.models import User
from database import get_db
from routers import EditUserValidator


# Создаем компонент
user_router = APIRouter(prefix='/users', tags=['Управление с пользователями'])


# Получить всех пользователей
def get_all_users_db():
    db = next(get_db())

    result = db.query(User).all()

    return result


@user_router.get('/all-user')
async def get_all_users():
    return get_all_users_db()


# Добавить нового юзера
def add_new_user_db(name, last_name, phone_number, email):
    db = next(get_db())

    user = User(name=name, last_name=last_name, phone_number=phone_number, email=email)
    db.add(user)
    db.commit()

    return user.user_id

@user_router.post('/add-new-user')
async def add_new_user(name, last_name, phone_number, email):
    user_id = add_new_user_db(name, last_name, phone_number, email)
    return {'user_id': user_id}


#  Удаления пользователя
def delete_user_db(user_id):
    db = next(get_db())
    user = db.query(User).filter_by(user_id=user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return f'Пользователь с ID {user_id} удален'
    else:
        return 'Пользователь не найден'


@user_router.delete('/delete-user')
async def delete_user(user_id):
    user = delete_user_db(user_id)
    return user


# Изменения данных пользователя
def edit_user_info_db(user_id, edit_info, new_info):
    db = next(get_db())

    exact_user = db.query(User).filter_by(user_id=user_id).first()  # 3

    if exact_user:
        if edit_info == 'name':
            exact_user.name = new_info
        elif edit_info == 'last_name':
            exact_user.last_name = new_info
        elif edit_info == 'email':
            exact_user.email = new_info
        elif edit_info == 'phone_number':
            exact_user.phone_number = new_info
        db.commit()
        return 'Данные успешно изменены!'
    else:
        return 'Пользователь не найден(('


@user_router.put('/edit')
async def edit_user_info(data: EditUserValidator):
    change_data = data.model_dump()
    result = edit_user_info_db(**change_data)
    return result


# Получить определенного пользователя
def get_exact_user_db(user_id):
    db = next(get_db())

    checker = db.query(User).filter_by(user_id=user_id).first()
    info = f'Name: {checker.name}, Last name {checker.last_name}, Email: {checker.email}, Phone number{checker.phone_number}'

    if checker:
        return f'Пользователь найден {info}'
    else:
        return 'Пользователь не обнаружен'


@user_router.get('/get-user')
async def get_exact_user(user_id):
    return get_exact_user_db(user_id)