from sqlalchemy import Column, String, Integer, DateTime, Date, Float, ForeignKey, TEXT
from sqlalchemy.orm import relationship

from database import Base


# Таблица пользователя
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    last_name = Column(String)
    phone_number = Column(Integer, unique=True)
    email = Column(String)

    reviews = relationship("BranchReview", back_populates="user")
    reports = relationship("Problem", back_populates="user")
    blocks = relationship("BlackList", back_populates="user")
    # связь со счетами
    invoices = relationship("Invoice", back_populates="user")
    test_drives = relationship("TestDrive", back_populates="user")

# Таблица Машин
class Car(Base):
    __tablename__ = 'cars'
    car_id = Column(Integer, primary_key=True, autoincrement=True)
    car_price = Column(Float)
    car_name = Column(String)
    car_company = Column(String)
    car_mileage = Column(Integer)
    car_color = Column(String)
    car_year = Column(Integer)
    car_photo = Column(String, nullable=True)

    test_drives = relationship("TestDrive", back_populates="car")
    insurances = relationship("Insurance", back_populates="car")

# Таблица Мотоциклов
class Motorbike(Base):
    __tablename__ = 'motorbikes'
    bike_id = Column(Integer, primary_key=True, autoincrement=True)
    bike_price = Column(Float)
    bike_name = Column(String)
    bike_company = Column(String)
    bike_mileage = Column(Integer)
    bike_color = Column(String)
    bike_year = Column(Integer)
    bike_photo = Column(String, nullable=True)


# Таблица автобусов
class Bus(Base):
    __tablename__ = 'buses'
    bus_id = Column(Integer, primary_key=True, autoincrement=True)
    bus_price = Column(Float)
    bus_name = Column(String)
    bus_company = Column(String)
    bus_mileage = Column(Integer)
    bus_color = Column(String)
    bus_year = Column(Integer)
    bus_photo = Column(String, nullable=True)



# Таблица филиалов
class Branch(Base):
    __tablename__ = 'branches'
    branch_id = Column(Integer, primary_key=True, autoincrement=True)
    branch_name = Column(String)
    address = Column(String)
    open_time = Column(String)
    closed_time = Column(String)
    phone_number = Column(String, unique=True)

    managers = relationship("Manager", back_populates="branch")
    reviews = relationship("BranchReview", back_populates="branch")
    reports = relationship("Report", back_populates="branch")
    problems = relationship("Problem", back_populates="branch")  # Исправлено
    agreements = relationship("Agreement", back_populates="branch")



# Таблица отзывов о филиале
class BranchReview(Base):
    __tablename__ = 'branch_reviews'
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, ForeignKey('branches.branch_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    review_text = Column(String)
    rating = Column(Integer)
    review_date = Column(DateTime)

    branch = relationship("Branch", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


# Таблица отдела кол-центра
class CenterDepartment(Base):
    __tablename__ = 'center_departments'
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String)
    department_lastname = Column(String)
    department_phone_number = Column(String, unique=True)


# Таблица маркетолога
class MarketDepartment(Base):
    __tablename__ ='market_departments'
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String)
    department_lastname = Column(String)
    department_phone_number = Column(String, unique=True)


# Таблица менеджера
class Manager(Base):
    __tablename__ ='managers'
    manager_id = Column(Integer, primary_key=True, autoincrement=True)
    manager_name = Column(String)
    manager_lastname = Column(String)
    manager_phone_number = Column(String, unique=True)
    department_branch = Column(Integer, ForeignKey('branches.branch_id'))

    branch = relationship("Branch", back_populates="managers")


# Таблица жалоб
class Problem(Base):
    __tablename__ = 'problems'
    problem_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    branch_id = Column(Integer, ForeignKey('branches.branch_id'))
    problem_text = Column(TEXT)
    problem_date = Column(DateTime)

    user = relationship("User", back_populates="reports")
    branch = relationship("Branch", back_populates="problems")  # Исправлено


# Таблица отчетов
class Report(Base):
    __tablename__ = 'reports'
    report_id = Column(Integer, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, ForeignKey('branches.branch_id'))
    report_file = Column(String)
    report_date = Column(DateTime)

    branch = relationship("Branch", back_populates="reports")


# Таблица заказов
class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_name = Column(String)
    order_count = Column(Integer)
    order_price = Column(Float)
    order_date = Column(DateTime)


# Таблица заявок от сайта
class WebSite(Base):
    __tablename__ = 'website_requests'
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    request_name = Column(String)
    request_email = Column(String)
    request_phone = Column(String)
    request_message = Column(TEXT)


# Таблица черный список клиентов
class BlackList(Base):
    __tablename__ = 'black_list'
    block_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship("User", back_populates="blocks")


# Таблица поставщиках
class Supplier(Base):
    __tablename__ ='suppliers'
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_company = Column(String)
    supplier_phone_number = Column(String, unique=True)
    supplier_email = Column(String, nullable=True)
    supplier_address = Column(String)


# Таблица договоров
class Agreement(Base):
    __tablename__ = 'agreements'
    agreement_id = Column(Integer, primary_key=True, autoincrement=True)
    branch_id = Column(Integer, ForeignKey('branches.branch_id'))
    agreement_file = Column(String)
    agreement_date = Column(DateTime)

    branch = relationship("Branch", back_populates="agreements")  # Исправлено


# Таблица сервисных услуг
class ServiceOffering(Base):
    __tablename__ = 'service_offerings'
    service_id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String)
    service_description = Column(TEXT)  # Описание услуги
    service_price = Column(Float)


# Таблица счетов
class Invoice(Base):
    __tablename__ = 'invoices'
    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))  # Ссылка на пользователя
    total_amount = Column(Float)   # Общая сумма
    issue_date = Column(DateTime)  # Дата выпуска счета
    due_date = Column(DateTime)    # Срок оплаты счета
    status = Column(String)        # Статус счета (например, "оплачен", "не оплачен")

    # Связь с пользователем
    user = relationship("User", back_populates="invoices")


# Таблица тест-драйвов
class TestDrive(Base):
    __tablename__ = 'test_drives'
    test_drive_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    car_id = Column(Integer, ForeignKey('cars.car_id'))
    scheduled_date = Column(DateTime)
    status = Column(String)

    user = relationship("User", back_populates="test_drives")
    car = relationship("Car", back_populates="test_drives")


# Таблица страховки
class Insurance(Base):
    __tablename__ = 'insurances'
    insurance_id = Column(Integer, primary_key=True, autoincrement=True)
    car_id = Column(Integer, ForeignKey('cars.car_id'))
    policy_number = Column(String, unique=True)
    provider = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    coverage_amount = Column(Float)
    status = Column(String)

    car = relationship("Car", back_populates="insurances")