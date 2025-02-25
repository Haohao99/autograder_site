from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, select

from db import engine
from models import User, Comment
from schemas import DeleteID

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.get("/api/sample")
def sample():
    return {"Hello": "World"}


@app.post("/comments/create")
def create_comment(comment: Comment):
    comment.id = None

    with Session(engine) as session:
        # make sure user_id exists
        user = session.get(User, comment.user_id)
        if not user:
            comment.user_id = None
        session.add(comment)
        session.commit()
        session.refresh(comment)
    return comment


@app.post("/comments/delete")
def delete_comment(delete_id: DeleteID):
    with Session(engine) as session:
        comment = session.get(Comment, delete_id.id)
        if not comment:
            raise HTTPException(status_code=400, detail="Comment not found")
        session.delete(comment)
        session.commit()
    return comment


@app.get("/comments")
def read_comment():
    with Session(engine) as session:
        heroes = session.exec(select(Comment)).all()
        return heroes


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def main():
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=5000)


if __name__ == "__main__":
    main()
