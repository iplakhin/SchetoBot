from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    pk: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)


class Income(Base):
    __tablename__ = "income"

    pk: Mapped[int] = mapped_column(primary_key=True)
    user_pk: Mapped[int] = mapped_column(ForeignKey("user.pk", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    title: Mapped[str]
    amount: Mapped[int]
    tag: Mapped[str] # total, my, extra, withdraw


class Price(Base):
    __tablename__ = 'price'

    pk: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    price: Mapped[int]
