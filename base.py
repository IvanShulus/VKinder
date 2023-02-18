from sqlalchemy import Column, Integer, String, ForeignKey, exc
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool


Base = declarative_base()
engine = create_async_engine('postgresql+asyncpg://postgres:123456@localhost:5432/vkinder', echo=False,
                             poolclass=NullPool)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    sex = Column(Integer, nullable=True)
    age = Column(Integer, nullable=True)
    city = Column(String, nullable=True)
    relation = Column(Integer, nullable=True)


class View(Base):
    __tablename__ = 'view'
    id = Column(Integer, primary_key=True)
    viewed_user = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    user = relationship(User, backref='views')


class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    liked_user = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

    user = relationship(User, backref='likes')


async def is_user(user_id):
    async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
        results = await session.execute(stmt)
        users = results.scalars().all()
    return True if users else False


async def is_viewed(user_id, viewed_user_id):
    async with async_session() as session:
        stmt = select(View).where(View.viewed_user == viewed_user_id, View.user_id == user_id)
        results = await session.execute(stmt)
        views = results.scalars().all()
    return True if views else False


async def get_user_from_db(user_id):
    async with async_session() as session:
        stmt = select(User).where(User.user_id == user_id)
        results = await session.execute(stmt)
        user = results.scalars().first()
    return user


async def add_new_user_in_db(user_id, age, sex_id, relation_id, city):
    user = User(user_id=user_id, age=age, sex=sex_id, city=city, relation=relation_id)
    async with async_session() as session:
        async with session.begin():
            session.add(user)
        try:
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()


async def add_view_in_db(user_id, viewed_user_id):
    view = View(user_id=user_id, viewed_user=viewed_user_id)
    async with async_session() as session:
        async with session.begin():
            session.add(view)
        try:
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()


async def add_like_in_db(user_id, liked_user_id):
    like = Like(user_id=user_id, liked_user=liked_user_id)
    async with async_session() as session:
        async with session.begin():
            session.add(like)
        try:
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
