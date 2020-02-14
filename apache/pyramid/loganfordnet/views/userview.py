from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import Allow, Everyone, forget

from .loganfordnetview import LoganFordNetView
from ..models import User, UserPermission, Permission

class UserView(LoganFordNetView):
    @view_config(route_name='user_view', renderer='../templates/user.pt', permission='view')
    def user_view(self):
        user = self.request.context.user
        self.response['user'] = user
        
        #Build a list of permissions given to the user
        self.response['permissions'] = self.get_effective_permissions(self.request.dbsession, user)
        
        return self.response

    @view_config(route_name='user_update_permissions', permission='edit')
    def user_update_permissions(self):
        user = self.request.context.user
        permissions = self.get_effective_permissions(self.request.dbsession, user)
        
        #Update the effective permissions
        for permission in permissions:
            if permission[0] in self.request.params:
                user.set_permission(permission[0], 1)
            else:
                user.set_permission(permission[0], 0)
        
        return HTTPFound(location=self.request.route_url('user_view', user_id = user.id))
        
    @view_config(route_name='user_list', renderer='../templates/userlist.pt', permission='list')
    def user_list(self):
        users = self.request.dbsession.query(User).all()
        self.response['users'] = users
        
        return self.response
    
    @view_config(route_name='user_delete', permission='delete')
    def user_delete(self):
        user_to_delete = self.request.context.user
        
        #if self.request.user.id == user_to_delete.id:
        #    self.alert('You cannot delete yourself.')
        #    return HTTPFound(location=self.request.route_url('user_view', user_id = user_to_delete.id))
        
        self.request.dbsession.delete(user_to_delete)
        self.alert('User has been deleted.')
        
        if self.request.user.id == user_to_delete.id:
            headers = forget(self.request)
            return HTTPFound(location=self.request.route_url('home'), headers=headers)
        
        return HTTPFound(location=self.request.route_url('home'))
        
    #Returns a list of tuples of the user's effective permissions, in the format (name, description, setting[0/1])
    def get_effective_permissions(self, dbsession, user):
        query_results = self.request.dbsession.query(Permission, UserPermission) \
        .outerjoin(UserPermission, (Permission.name == UserPermission.name) & (UserPermission.user_id == user.id)) \
        .all()
            
        permissions = []
        for i in query_results:
            permissions.append((i[0].name, i[0].description, 0 if i[1] is None else i[1].setting))
        
        return permissions


#ACL
def user_page_factory(request):
    return UserPageResource()
    
class UserPageResource(object):
    def __acl__(self):
        return [
            (Allow, 'perm:admin.user', 'list'),
        ]

def user_model_factory(request):
    user_id = request.matchdict['user_id']
    user = request.dbsession.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPNotFound
    return UserModelResource(user)
        
class UserModelResource(object):
    def __init__(self, user):
        self.user = user
    
    def __acl__(self):
        return [
            (Allow, str(self.user.id), 'view'),
            (Allow, 'perm:admin.user', 'view'),
            (Allow, 'perm:admin.user', 'edit'),
            (Allow, str(self.user.id), 'delete'),
            (Allow, 'perm:admin.user', 'delete'),
        ]
