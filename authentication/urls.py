from django.urls import path
from .views import auth, user, test

# URLs para autenticación
auth_patterns = [
    path('login/', auth.login, name='auth-login'),
    path('logout/', auth.logout, name='auth-logout'),
]

# URLS para gestión de usuarios
user_patterns = [
    path('info/', user.get_user_info, name='user-info'),
    path('list/', user.get_user_list, name='user-list'),
    path('create/', user.create_user, name='user-create'),
]

# URL para página de prueba
test_patterns = [
    path('test/', test.api_test, name='api-test'),
]

urlpatterns = auth_patterns + user_patterns + test_patterns 