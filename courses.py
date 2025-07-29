from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from auth import get_current_user
from database import get_db

router = APIRouter()

class Course(BaseModel):
    title: str
    description: str

@router.post("/courses")
def create_course(course: Course, user: str = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO courses (title, description, owner) VALUES (?, ?, ?)",
                (course.title, course.description, user))
    conn.commit()
    return {"msg": "Course created"}

@router.get("/courses")
def get_courses(user: str = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM courses WHERE owner=?", (user,))
    return cur.fetchall()

@router.delete("/courses/{course_id}")
def delete_course(course_id: int, user: str = Depends(get_current_user)):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM courses WHERE id=? AND owner=?", (course_id, user))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Course not found or access is denied")

    return {"detail": "Course deleted!"}