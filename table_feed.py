from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from table_post import Post
from table_user import User


class Feed(Base):
    __tablename__ = "feed_action"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, name="user_id")
    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True, name="post_id")
    action = Column(String)
    time = Column(TIMESTAMP)

    user = relationship(User)
    post = relationship(Post)


