from pyramid.security import remember
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

from .loganfordnetview import LoganFordNetView

from ..models import User

class LogInView(LoganFordNetView):
    @view_config(route_name='log_in', renderer='../templates/login.pt')
    def log_in(self):
        if self.request.method == 'POST':
            failed = False
            
            username = self.request.params['username']
            password = self.request.params['password']
            
            user = self.request.dbsession.query(User).filter_by(name=username).first()
            
            if user == None or not user.check_password(password):
                self.alert('Incorrect username or password.')
                failed = True;
            
            if not failed:
                #Log in sucessful
                tokens = []
                for user_permission in user.permissions:
                    if user_permission.setting == 1:
                        tokens.append(str(user_permission.name))

                headers = remember(self.request, user.id, tokens=tokens)
                
                new_headers = []
                for header in headers:
                    if header[0] == 'Set-Cookie' and header[1].startswith('auth_tkt'):
                        headerl = list(header)
                        headerl[1] = headerl[1].replace('\\054', ',')
                        print(headerl)
                        header = tuple(headerl)
                    
                    new_headers.append(header)

                return HTTPFound(location=self.request.route_url('home'), headers=new_headers)
            else:
                return self.response
        
        return self.response
