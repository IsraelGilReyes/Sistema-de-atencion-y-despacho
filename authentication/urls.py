from django.urls import path
from authentication import views

urlpatterns = [
    # Autenticación
    path('login/', views.LoginView.as_view, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Usuarios
    path('info/', views.get_user_info, name='user-info'),
    path('list/', views.get_user_list, name='user-list'),
    path('create/', views.create_user, name='user-create'),
    
    # Roles
    path('roles/', views.role_list, name='role-list'),
    path('roles/create/', views.create_role, name='role-create'),
    path('roles/user/', views.get_user_roles, name='user-roles'),
    path('roles/assign/', views.assign_role, name='role-assign'),
]