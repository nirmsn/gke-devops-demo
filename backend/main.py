from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import os

app = FastAPI()

class User(BaseModel):
    name: str
    email: str

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user="root",
        password="password",
        database="demo"
    )

@app.post("/api/submit")
def submit(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100))"
    )
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (user.name, user.email)
    )
    conn.commit()
    conn.close()
    return {"message": "Stored successfully"}
