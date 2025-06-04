from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    """全モデルが継承するベースクラス"""
    pass


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)