from .views.userview import user_page_factory, user_model_factory
from .views.pagemaintenanceview import page_maintenance_page_factory, page_maintenance_model_factory

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('sign_up', '/sign_up/')
    config.add_route('log_in', '/log_in/')
    config.add_route('log_out', '/log_out/')
    
    config.add_route('user_view', '/user/{user_id}/', factory = user_model_factory)
    config.add_route('user_list', '/user/', factory = user_page_factory)
    config.add_route('user_update_permissions', '/user/{user_id}/update_permissions/', factory = user_model_factory)
    config.add_route('user_delete', '/user/{user_id}/delete/', factory = user_model_factory)
    
    config.add_route('ten_man', '/ten_man/')
    
    config.add_route('page_maintenance_list', '/page_maintenance/', factory = page_maintenance_page_factory)
    config.add_route('page_maintenance_create', '/page_maintenance/create/', factory = page_maintenance_page_factory)
    config.add_route('page_maintenance_edit', '/page_maintenance/{page_id}/edit/', factory = page_maintenance_model_factory)
    config.add_route('page_maintenance_delete', '/page_maintenance/{page_id}/delete/', factory = page_maintenance_model_factory)
    config.add_route('page_view', '/*page_name') #Must be last entry
    
    
