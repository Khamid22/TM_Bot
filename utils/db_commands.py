from pytz import timezone
from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from loader import db_session
from sqlalchemy import select

Base = declarative_base()

uz_timezone = timezone('Asia/Tashkent')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=True)
    name = Column(String)
    tg_id = Column(BigInteger, unique=True)
    joined_time = Column(DateTime, server_default=func.now(tz=uz_timezone))
    invited_friends = Column(Integer, default=0)


async def get_user_by_id(user_id):
    async with db_session() as session:
        stmt = select(User).where(User.tg_id == user_id)
        result = session.execute(stmt)
        user = result.scalar()
    return user


async def add_user(username, name, tg_id):
    user = User(username=username, name=name, tg_id=tg_id)
    async with db_session() as session:
        session.add(user)
        session.commit()


async def count_users():
    async with db_session() as session:
        stmt = select(func.count().label('user_count')).select_from(User)
        result = session.execute(stmt)
        user_count = result.scalar()
    return user_count


async def delete_all_users():
    async with db_session() as session:
        session.query(User).delete()
        session.commit()


async def update_user(user):
    async with db_session() as session:
        session.merge(user)
        session.commit()
