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
                headers = remember(self.request, user.id)
                return HTTPFound(location=self.request.route_url('home'), headers=headers)
            else:
                return self.response
        
        return self.response