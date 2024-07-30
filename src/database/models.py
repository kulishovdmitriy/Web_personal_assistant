import enum
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, generics
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy import String, ForeignKey, func, Enum
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
    user_id: Mapped[generics.UUID] = mapped_column(generics.UUID(), ForeignKey("user.id"), nullable=True)
    user: Mapped["User"] = relationship("User", backref="contacts", lazy="joined")


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)
    birthday: Mapped[date] = mapped_column("birthday", Date, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    create_at: Mapped[date] = mapped_column("create_at", DateTime, default=func.now())
    update_at: Mapped[date] = mapped_column("update_at", DateTime, default=func.now(), onupdate=func.now())
    blocked: Mapped[bool] = mapped_column(default=False)
    role: Mapped[Enum] = mapped_column("role", Enum(Role), default=Role.user, nullable=True)
