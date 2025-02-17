from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import count

from schema import UserGet, PostGet, FeedGet
from database import SessionLocal
from table_user import User
from table_post import Post
from table_feed import Feed

app = FastAPI()


def get_db():
    with SessionLocal() as db:
        return db


@app.get("/user/{id}", response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    answer = db.query(User).filter(User.id == id).one_or_none()

    if answer is None:
        raise HTTPException(404)
    return answer


@app.get("/post/{id}", response_model=PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    answer = db.query(Post).filter(Post.id == id).one_or_none()

    if answer is None:
        raise HTTPException(404)
    return answer


@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_user_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    answer = db.query(Feed).filter(Feed.user_id == id).order_by(Feed.time.desc()).limit(limit).all()

    if answer is None:
        return HTTPException(200, [])
    return answer


@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_post_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    answer = db.query(Feed).filter(Feed.post_id == id).order_by(Feed.time.desc()).limit(limit).all()

    if answer is None:
        return HTTPException(200, [])
    return answer


""" FOR FINAL PROJECT """


@app.get("/post/recommendations/")
def get_recommendations(id: int = None, limit: int = 10, db: Session = Depends(get_db)):
    request = db.query(Post.id, Post.text, Post.topic).select_from(Feed)\
        .filter(Feed.action == "like")\
        .join(Post)\
        .group_by(Post.id)\
        .order_by(count(Post.id).desc())\
        .limit(limit).all()

    return request