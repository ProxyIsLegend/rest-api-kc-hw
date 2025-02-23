from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.functions import count


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)


if __name__ == "__main__":
    session = SessionLocal()
    result = session.query(User.country, User.os, count("*"))\
        .filter(User.exp_group == 3)\
        .group_by(User.country)\
        .group_by(User.os)\
        .having(count("*") > 100)\
        .order_by(count("*").desc())\
        .all()

    print(result)