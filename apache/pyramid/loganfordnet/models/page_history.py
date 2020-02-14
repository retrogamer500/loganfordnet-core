import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, reconstructor
from sqlalchemy.dialects.mysql import TEXT, INTEGER, VARCHAR, TIMESTAMP

from .meta import Base

class PageHistory(Base):
    __tablename__ = 'page_history'
    id = Column(INTEGER, primary_key=True, index=True)
    content = Column(TEXT)
    version = Column(INTEGER, nullable=False)
    last_modified_by_id = Column(INTEGER, ForeignKey('user.id'), nullable=False)
    last_modified_by = relationship("User")
    last_modified_date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    page_id = Column(INTEGER, ForeignKey('page.id'), nullable=False)
    page = relationship("Page", back_populates="history")
