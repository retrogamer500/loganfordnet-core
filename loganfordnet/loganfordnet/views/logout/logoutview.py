from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget
from pyramid.view import view_config
from ..loganfordnetview import LoganFordNetView

class LogOutView(LoganFordNetView):
    @view_config(route_name='log_out')
    def log_out(self):
        headers = forget(self.request)
        return HTTPFound(location=self.request.route_url('home'), headers=headers)
