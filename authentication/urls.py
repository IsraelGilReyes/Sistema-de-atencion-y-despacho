from django.urls import path
from .views import auth, user, role

urlpatterns = [
    # Autenticación
    path('login/', auth.login, name='auth-login'),
    path('logout/', auth.logout, name='auth-logout'),
    
    # Usuarios
    path('info/', user.get_user_info, name='user-info'),
    path('list/', user.get_user_list, name='user-list'),
    path('create/', user.create_user, name='user-create'),
    
    # Roles
    path('roles/', role.role_list, name='role-list'),
    path('roles/create/', role.create_role, name='role-create'),
    path('roles/user/', role.get_user_roles, name='user-roles'),
    path('roles/assign/', role.assign_role, name='role-assign'),
]