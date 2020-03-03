import bcrypt
import datetime
import ldap
import ldap.modlist
import logging

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, reconstructor
from sqlalchemy.dialects.mysql import TEXT, INTEGER, VARCHAR, TIMESTAMP

from .user_permission import UserPermission

from .meta import Base

log = logging.getLogger(__name__)

class User(Base):
    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(VARCHAR(length=100, charset='utf8mb4'), nullable=False, unique=True)
    role = Column(TEXT(length=100, charset='utf8mb4'), nullable=False)
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
        
    def create_ldap_user(self, pw, settings):
        con = ldap.initialize('ldap://openldap')
        con.simple_bind_s("cn=admin,dc=loganford,dc=net", settings['ldap.password'])

        dn = "uid=" + self.name + ",ou=users,dc=loganford,dc=net"
        ldap_pw = '{BCRYPT}' + bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt()).decode("utf-8") 
        modlist = {
            "objectClass": [str.encode('person'), str.encode('extensibleObject')],
            "sn": [str.encode(self.name)],
            "cn": [str.encode(self.name)],
            "userPassword": [str.encode(ldap_pw)]
        }
        
        result = con.add_s(dn, ldap.modlist.addModlist(modlist))

    def check_ldap_password(self, pw, settings):
        con = ldap.initialize('ldap://openldap')
        try:
            con.simple_bind_s("uid=" + self.name + ",ou=users,dc=loganford,dc=net", pw)
            return True
        except ldap.INVALID_CREDENTIALS as err:
            log.info('Invalid credentials: ' + str(err))
        except ldap.LDAPError as err:
            log.info('Other LDAP error: ' + str(err))
        except:
            log.info('Error while logging in: ' + str(sys.exc_info()[0]))
        return False

    def set_ldap_permissions(self, settings):
        con = ldap.initialize('ldap://openldap')
        con.simple_bind_s("cn=admin,dc=loganford,dc=net", settings['ldap.password'])
        dn = "uid=" + self.name + ",ou=users,dc=loganford,dc=net"

        #Delete old stuff
        try:
            con.modify_s(dn, [(ldap.MOD_DELETE, 'info', None)])
        except ldap.NO_SUCH_ATTRIBUTE:
            log.info('No user info exists')

        #Add new stuff
        perms_to_add = []
        for user_permission in self.permissions:
            if user_permission.setting == 1 and user_permission.id is not None:
                perms_to_add.append(str.encode(user_permission.name))

        if len(perms_to_add) > 0:
            con.modify_s(dn, [(0, 'info', perms_to_add)])
    
    def delete_ldap_user(self, settings):
        con = ldap.initialize('ldap://openldap')
        con.simple_bind_s("cn=admin,dc=loganford,dc=net", settings['ldap.password'])
        dn = "uid=" + self.name + ",ou=users,dc=loganford,dc=net"
        con.delete_s(dn)