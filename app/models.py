from sqlalchemy import Column, Integer, String
from .database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_url = Column(String, unique=True, index=True)
    stats = Column(Integer, index=True)
