import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, reconstructor
from sqlalchemy.dialects.mysql import TEXT, INTEGER, VARCHAR, TIMESTAMP

from .meta import Base

class Page(Base):
    __tablename__ = 'page'
    id = Column(INTEGER, primary_key=True, index=True)
    title = Column(VARCHAR(length=100, charset='utf8mb4'), nullable=False, unique=False)
    url = Column(VARCHAR(length=256, charset='utf8mb4'), nullable=False, unique=True)
    display_in_sidebar = Column(INTEGER, nullable=False)
    created_by_id = Column(INTEGER, ForeignKey('user.id'), nullable=False)
    created_by = relationship("User")
    created_date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    history = relationship("PageHistory", back_populates="page", order_by="desc(PageHistory.version)", cascade="all, delete-orphan")
