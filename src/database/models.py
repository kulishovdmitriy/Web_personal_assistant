import enum
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey, func, Enum
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


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    birthday: Mapped[date] = mapped_column("birthday", Date, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    create_at: Mapped[date] = mapped_column("create_at", DateTime, default=func.now())
    update_at: Mapped[date] = mapped_column("update_at", DateTime, default=func.now(), onupdate=func.now())
    blocked: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Enum] = mapped_column("role", Enum(Role), default=Role.user, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
