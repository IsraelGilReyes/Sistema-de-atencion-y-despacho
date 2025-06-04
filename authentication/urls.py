from django.urls import path
from .views import auth, user, role

# URLs para autenticación
auth_patterns = [
    path('login/', auth.login, name='auth-login'),
    path('logout/', auth.logout, name='auth-logout'),
]

# URLs para gestión de usuarios
user_patterns = [
    path('info/', user.get_user_info, name='user-info'),
    path('list/', user.get_user_list, name='user-list'),
    path('create/', user.create_user, name='user-create'),
]

# URLs para gestión de roles
role_patterns = [
    path('roles/', role.role_list, name='role-list'),
    path('roles/create/', role.create_role, name='role-create'),
    path('roles/user/', role.get_user_roles, name='user-roles'),
    path('roles/assign/', role.assign_role, name='role-assign'),
]

urlpatterns = auth_patterns + user_patterns + role_patterns 