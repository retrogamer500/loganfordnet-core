from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models

from .loganfordnetview import LoganFordNetView

class HomeView(LoganFordNetView):
    @view_config(route_name='home', renderer='../templates/home.pt')
    def home(self):
        return self.response
