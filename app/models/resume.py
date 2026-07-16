from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from datetime import datetime

from app.core.database import Base


class Resume(Base):

    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    original_filename: Mapped[str] = mapped_column(String)

    saved_filename: Mapped[str] = mapped_column(String)

    name: Mapped[str] = mapped_column(String)

    email: Mapped[str] = mapped_column(String)

    phone: Mapped[str] = mapped_column(String)

    resume_json: Mapped[dict] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )