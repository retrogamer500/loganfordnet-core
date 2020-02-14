from pyramid.view import view_config
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from .. import models

from .loganfordnetview import LoganFordNetView

class TenManView(LoganFordNetView):
    @view_config(route_name='ten_man', renderer='../templates/tenman.pt')
    def ten_man(self):
        return self.response
