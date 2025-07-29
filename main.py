from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users import router as users_router
from courses import router as courses_router
from models import create_tables

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users_router)
app.include_router(courses_router)


@app.on_event("startup")
def startup():
    create_tables()
