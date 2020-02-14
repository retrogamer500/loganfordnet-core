from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import Allow, Everyone, forget

from .loganfordnetview import LoganFordNetView

from ..models import Page, PageHistory

class PageMaintenanceView(LoganFordNetView):
    @view_config(route_name='page_maintenance_list', renderer='../templates/pagemaintenancelist.pt', permission='list')
    def page_maintenance_list(self):
        pages = self.request.dbsession.query(Page).all()
        self.response['pages'] = pages
        
        return self.response
    
    @view_config(route_name='page_maintenance_create', renderer='../templates/pagecreate.pt', permission='create')
    def page_maintenance_create(self):
        
        if self.request.method == 'POST':
            page_name = self.request.params['page_name']
            page_url = self.request.params['page_url']
            display_in_sidebar = 1 if 'display_in_sidebar' in self.request.params else 0
            content = self.request.params['content']
            
            #Todo: additional validations
            
            #Format URL
            if page_url[0] != '/':
                page_url = '/' + page_url
            if page_url[-1] != '/':
                page_url = page_url + '/'
            
            new_page = Page(title=page_name, url=page_url, display_in_sidebar=display_in_sidebar, created_by=self.request.user)
            new_page_history = PageHistory(content=content, last_modified_by=self.request.user, page=new_page, version=0)

            self.request.dbsession.add(new_page)
            self.alert('Page \'' + page_name +'\' created!')
            return HTTPFound(location=self.request.route_url('page_maintenance_list'))
        
        return self.response
        
    @view_config(route_name='page_view', renderer='../templates/pageview.pt')
    def page_view(self):
        route = '/'
        for string in self.request.matchdict['page_name']:
            if len(string) > 0:
                route+=(string+'/')
        
        #Search for page with route
        page = self.request.dbsession.query(Page).filter_by(url=route).first()
        if page is not None:
            self.response['page'] = page
            return self.response
        else:
            raise HTTPNotFound()
            
    @view_config(route_name='page_maintenance_delete', permission='delete')
    def page_maintenance_delete(self):
        page_to_delete = self.request.context.page
        
        self.request.dbsession.delete(page_to_delete)
        self.alert('Page deleted!')
        return HTTPFound(location=self.request.route_url('page_maintenance_list'))
        
    
    @view_config(route_name='page_maintenance_edit', renderer='../templates/pageedit.pt', permission='edit')
    def page_maintenance_edit(self):
        page_to_edit = self.request.context.page
        
        if self.request.method == 'POST':
            
            page_name = self.request.params['page_name']
            page_url = self.request.params['page_url']
            display_in_sidebar = 1 if 'display_in_sidebar' in self.request.params else 0
            content = self.request.params['content']
            
            #Todo: additional validations
            
            page_to_edit.title = page_name
            page_to_edit.url = page_url
            page_to_edit.display_in_sidebar = display_in_sidebar
            
            #Create history entry
            new_page_history = PageHistory(content=content, last_modified_by=self.request.user, page=page_to_edit, version=page_to_edit.history[0].version+1)
            
            return HTTPFound(location=self.request.route_url('page_maintenance_list'))
        else:
            self.response['page']= page_to_edit
            return self.response
        
#ACL
def page_maintenance_page_factory(request):
    return PageMaintenancePageResource()
    
class PageMaintenancePageResource(object):
    def __acl__(self):
        return [
            (Allow, 'perm:pages.admin', 'list'),
            (Allow, 'perm:pages.admin', 'create'),
        ]

def page_maintenance_model_factory(request):
    page_id = request.matchdict['page_id']
    page = request.dbsession.query(Page).filter_by(id=page_id).first()
    if page is None:
        raise HTTPNotFound
    return PageMaintenanceModelResource(page)
        
class PageMaintenanceModelResource(object):
    def __init__(self, page):
        self.page = page
    
    def __acl__(self):
        return [
            (Allow, 'perm:pages.admin', 'delete'),
            (Allow, 'perm:pages.admin', 'edit'),
        ]
