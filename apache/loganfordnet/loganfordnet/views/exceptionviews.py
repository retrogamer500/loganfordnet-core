from pyramid.view import notfound_view_config, forbidden_view_config

from .loganfordnetview import LoganFordNetView

class ExceptionViews(LoganFordNetView):
    @notfound_view_config(renderer='../templates/404.pt')
    def notfound_view(self):
        self.request.response.status = 404
        return self.response
        
    @forbidden_view_config(renderer='../templates/403.pt')
    def forbidden_view(self):
        self.request.response.status = 403
        return self.response
