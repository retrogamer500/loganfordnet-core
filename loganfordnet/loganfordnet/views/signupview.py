from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError

from .. import models
from ..models import User
from .loganfordnetview import LoganFordNetView

import re

username_regex = '^[a-zA-Z0-9_]+$'

class SignUpView(LoganFordNetView):
    @view_config(route_name='sign_up', renderer='../templates/signup.pt')
    def sign_up(self):
        if self.request.method == 'POST':
            failed = False
            
            username = self.request.params['username']
            password = self.request.params['password']
            confirm_password = self.request.params['confirm_password']
            site_code = self.request.params['site_code']
            
            user = self.request.dbsession.query(User).filter_by(name=username).first()
            if user != None:
                self.alert('Username ' + username + ' already exists.')
                failed = True
                
            if len(username) <= 3:
                self.alert('Username must be greater than 3 characters.')
                failed = True
            
            if len(username) > 40:
                self.alert('Username must not be longer than 40 characters.')
                failed = True
                
            if len(password) <= 5:
                self.alert('Password must be greater than 5 characters.')
                failed = True
            
            if not re.match(username_regex, username):
                self.alert('Invalid username! Valid characters are letters, numbers, and underscores.')
                failed = True
            
            if password != confirm_password:
                self.alert('Passwords do not match.')
                failed = True
                
            if site_code != 'jumpthrow':
                self.alert('Site code is incorrect.')
                failed = True
            
            if not failed:
                new_user = User(name=username, role='user')
                new_user.set_password(password)
                self.request.dbsession.add(new_user)
                self.alert('Account \'' + username +'\' created!')
                return HTTPFound(location=self.request.route_url('log_in'))
                
        return self.response
