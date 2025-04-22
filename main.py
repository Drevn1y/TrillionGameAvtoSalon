from fastapi import FastAPI
from routers.user_api import user_router
from routers.car_api import car_router
from routers.motorbike_api import motorbike_router
from routers.bus_api import bus_router
from routers.branch_api import branch_router
from routers.rewiew_api import branch_review_router
from routers.center_department_api import center_department_router
from routers.market_department_api import market_department_router
from routers.manager_api import manager_router
from routers.problem import problem_router
from routers.report_api import reports_router
from routers.agreement_api import agreement_router
from routers.orders_api import orders_router
from routers.website_requests_api import website_router
from routers.blacklist_api import blacklist_router
from routers.suppliers_api import suppliers_router
from routers.service_offerings_api import services_router
from routers.invoice_api import invoice_router
from routers.testdrive_api import testdrive_router
from routers.insurance_api import insurance_router


from database import Base, engine
Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url='/')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать конкретные адреса, например ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т. д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(user_router)
app.include_router(car_router)
app.include_router(motorbike_router)
app.include_router(bus_router)
app.include_router(branch_router)
app.include_router(branch_review_router)
app.include_router(center_department_router)
app.include_router(market_department_router)
app.include_router(manager_router)
app.include_router(problem_router)
app.include_router(reports_router)
app.include_router(agreement_router)
app.include_router(orders_router)
app.include_router(website_router)
app.include_router(blacklist_router)
app.include_router(suppliers_router)
app.include_router(services_router)
app.include_router(invoice_router)
app.include_router(testdrive_router)
app.include_router(insurance_router)


