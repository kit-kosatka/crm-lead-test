from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(30))

    source: Mapped[str] = mapped_column(String(20))
    manager: Mapped[str] = mapped_column(String(20))
    stage: Mapped[str] = mapped_column(String(50))

    requested_tz: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
