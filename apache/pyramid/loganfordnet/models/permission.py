from sqlalchemy import Column, Integer, Text, ForeignKey
from .meta import Base

from sqlalchemy.dialects.mysql import TEXT, INTEGER, VARCHAR, TIMESTAMP

import datetime

class Permission(Base):
    __tablename__ = 'permission'
    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(VARCHAR(length=64, charset='utf8mb4'), nullable=False, unique=True, index=True)
    group = Column(VARCHAR(length=64, charset='utf8mb4'), nullable=False)
    description = Column(VARCHAR(length=256, charset='utf8mb4'), nullable=False)
