from ..models import Page

class LoganFordNetView(object):
    def __init__(self, request):
        self.request = request
        self.response = {}
        
        #Load sidebar
        custom_pages = self.request.dbsession.query(Page).filter_by(display_in_sidebar=1).all()
        self.response['custom_pages'] = custom_pages
        
    def alert(self, message):
        print('Flashing message!');
        self.request.session.flash(message)
