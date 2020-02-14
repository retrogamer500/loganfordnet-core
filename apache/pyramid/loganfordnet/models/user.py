import bcrypt
import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, reconstructor
from sqlalchemy.dialects.mysql import TEXT, INTEGER, VARCHAR, TIMESTAMP

from .user_permission import UserPermission

from .meta import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(VARCHAR(length=100, charset='utf8mb4'), nullable=False, unique=True)
    role = Column(TEXT(length=100, charset='utf8mb4'), nullable=False)
    password_hash = Column(TEXT(length=512))
    created_date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    permissions = relationship("UserPermission", back_populates="user")
        
    def permission_enabled(self, name):
        for user_permission in self.permissions:
            if user_permission.name == name:
                return user_permission.setting == 1
        return False
        
    def set_permission(self, name, setting):
        found = False
        for user_permission in self.permissions:
            if user_permission.name == name:
                user_permission.setting = 1 if setting else 0
                found = True
        
        if not found and setting == True:
            user_permission = UserPermission(name=name, user=self, setting=1)
            self.permissions.append(user_permission)
        

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False
