from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy import String, ForeignKey, Boolean, func, Integer
from datetime import date
from sqlalchemy.sql.sqltypes import DateTime, Date

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(String(250))
    number_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    birthday: Mapped[date] = mapped_column("birthday", Date, nullable=False)
    create_at: Mapped[date] = mapped_column("create_at", DateTime, default=func.now(), nullable=True)
    update_at: Mapped[date] = mapped_column("update_at", DateTime, default=func.now(), onupdate=func.now(),
                                            nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", backref="contacts", lazy="joined")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(75), nullable=False, unique=True)
    birthday: Mapped[date] = mapped_column("birthday", Date, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    create_at: Mapped[date] = mapped_column("create_at", DateTime, default=func.now())
    update_at: Mapped[date] = mapped_column("update_at", DateTime, default=func.now(), onupdate=func.now())
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    blocked: Mapped[bool] = mapped_column(default=False)
