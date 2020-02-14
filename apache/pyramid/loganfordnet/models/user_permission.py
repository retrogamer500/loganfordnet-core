from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .meta import Base

from sqlalchemy.dialects.mysql import TEXT, INTEGER, VARCHAR, TIMESTAMP

import datetime

class UserPermission(Base):
    __tablename__ = 'user_permission'
    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(VARCHAR(length=64, charset='utf8mb4'), ForeignKey('permission.name'), nullable=False, index=True)
    setting = Column(INTEGER, nullable=False, default=0)
    user_id = Column(INTEGER, ForeignKey('user.id'))
    user = relationship("User", back_populates="permissions")
