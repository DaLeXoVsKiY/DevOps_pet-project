from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg
import os

def get_connection():
    return psycopg.connect(
        host="db",
        port=5432,
        dbname="app_db",
        user="root",
        password="db123"
    )


app = FastAPI(title="Task Board API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tasks")
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, completed FROM tasks ORDER BY id"
    )

    rows = cursor.fetchall()

    tasks = [
        {
            "id": row[0],
            "title": row[1],
            "completed": row[2]
        }
        for row in rows
    ]

    cursor.close()
    conn.close()

    return tasks


@app.post("/api/tasks")
def create_task(task: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, completed)
        VALUES (%s, false)
        RETURNING id, title, completed
        """,
        (task["title"],)
    )

    new_task = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": new_task[0],
        "title": new_task[1],
        "completed": new_task[2]
    }


@app.patch("/api/tasks/{task_id}")
def toggle_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = NOT completed
        WHERE id = %s
        RETURNING id, title, completed
        """,
        (task_id,)
    )

    updated_task = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    if updated_task is None:
        return {"error": "Task not found"}

    return {
        "id": updated_task[0],
        "title": updated_task[1],
        "completed": updated_task[2]
    }


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = %s
        RETURNING id
        """,
        (task_id,)
    )

    deleted_task = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    if deleted_task is None:
        return {"error": "Task not found"}

    return {"message": "Task deleted"}
