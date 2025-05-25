import datetime, time

from sqlalchemy import BigInteger, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
# from datetime import date, datetime, time

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id_user: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    date_reg = mapped_column(DateTime,default=datetime.datetime.now())

class Key(Base):
    __tablename__ = 'keys'

    id_key: Mapped[int] = mapped_column(primary_key=True)
    text_key: Mapped[str] = mapped_column(String(2500))
    type_key: Mapped[int]
    used: Mapped[bool] = mapped_column(default=False)
    need_deactivate: Mapped[bool] = mapped_column(default=False)

class Key_User(Base):
    __tablename__ = 'key_user'

    id_user: Mapped[int]  = mapped_column(primary_key=True)
    type_key: Mapped[int] = mapped_column(primary_key=True)
    id_key: Mapped[int]
    # name: Mapped[str] = mapped_column(String(25))
    # description: Mapped[str] = mapped_column(String(2200))
    # price: Mapped[int] = mapped_column()
    # category: Mapped[int] = mapped_column(ForeignKey('categories.id'))

class User_profile(Base):
    __tablename__ = 'users_profile'

    id_user: Mapped[int] = mapped_column(primary_key=True)
    sub_date_from = mapped_column(DateTime,nullable=True)
    sub_date_to = mapped_column(DateTime,nullable=True)
    freeweek: Mapped[bool] = mapped_column(default=False)
    # freeweek_used: Mapped[bool] = mapped_column(default=False)
    mobile: Mapped[int] #1-IOS 2-Android
    # sub_date_to: Mapped[datetime] = mapped_column(datetime)

class Payments(Base):
    __tablename__ = 'payments'

    id_payments: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    id_user: Mapped[int]
    telegram_payment_charge_id: Mapped[String] = mapped_column(String(1000))
    total_amount: Mapped[int]
    date_payments = mapped_column(DateTime)
    refund: Mapped[bool] = mapped_column(default=False)

class Type_key(Base):
    __tablename__ = 'type_key'

    type_key: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(100))

async def asunc_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)