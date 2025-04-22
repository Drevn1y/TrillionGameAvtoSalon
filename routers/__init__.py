from datetime import datetime

from pydantic import BaseModel


# Валидатор для редактирования
class EditUserValidator(BaseModel):
    user_id: int
    edit_info: str
    new_info: str


# Схема данных для добавления новой машины
class CarValidator(BaseModel):
    car_price: float
    car_name: str
    car_company: str
    car_mileage: int
    car_color: str
    car_year: int


# Схема данных для добавления нового мотоцикла
class MotorbikeValidator(BaseModel):
    bike_price: float
    bike_name: str
    bike_company: str
    bike_mileage: int
    bike_color: str
    bike_year: int


# Схема данных для добавления нового автобуса
class BusValidator(BaseModel):
    bus_price: float
    bus_name: str
    bus_company: str
    bus_mileage: int
    bus_color: str
    bus_year: int


# Pydantic модель для добавления и обновления филиала
class BranchCreateUpdate(BaseModel):
    branch_name: str
    address: str
    open_time: str
    closed_time: str
    phone_number: str


# Pydantic модель для добавления и обновления отзыва
class BranchReviewCreateUpdate(BaseModel):
    branch_id: int
    user_id: int
    review_text: str
    rating: int
    review_date: datetime = datetime.now()


# Pydantic модель для добавления и обновления отдела
class CenterDepartmentCreateUpdate(BaseModel):
    department_name: str
    department_lastname: str
    department_phone_number: str


# Pydantic модель для добавления и обновления отдела
class MarketDepartmentCreateUpdate(BaseModel):
    department_name: str
    department_lastname: str
    department_phone_number: str


# Pydantic модель для добавления и обновления менеджера
class ManagerCreateUpdate(BaseModel):
    manager_name: str
    manager_lastname: str
    manager_phone_number: str
    department_branch: int


# Pydantic модель для добавления и обновления жалобы
class ProblemCreateUpdate(BaseModel):
    user_id: int
    branch_id: int
    problem_text: str
    problem_date: datetime = datetime.now()

