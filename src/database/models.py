from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from sqlalchemy import String, ForeignKey, Boolean, func
from datetime import date
from sqlalchemy.sql.sqltypes import DateTime, Integer

Base = declarative_base()


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(75), nullable=False, unique=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    create_at: Mapped[date] = mapped_column("create_at", DateTime, default=func.now())
    update_at: Mapped[date] = mapped_column("update_at", DateTime, default=func.now(), onupdate=func.now())
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    blocked: Mapped[bool] = mapped_column(default=False)
