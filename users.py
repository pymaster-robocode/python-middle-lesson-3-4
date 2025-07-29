from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import get_db
from auth import create_access_token, get_current_user
from passlib.hash import bcrypt

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: User):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                    (user.username, bcrypt.hash(user.password)))
        conn.commit()
    except:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"msg": "User created"}

@router.post("/login")
def login(user: User):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (user.username,))
    row = cur.fetchone()
    if not row or not bcrypt.verify(user.password, row["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"username": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me") # Task
def read_me(username: str = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses WHERE owner=?", (username,))
    data = len(cur.fetchall())
    return {"username": username, "courses": data}