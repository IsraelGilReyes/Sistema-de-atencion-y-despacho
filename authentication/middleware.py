# authentication/middleware.py
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import resolve
from django.conf import settings

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs que no requieren autenticación
        self.public_urls = [
            '/api/auth/login/',
            '/api/auth/register/',
            '/api/auth/token/refresh/',
            '/admin/',
            '/static/',
        ]

    def __call__(self, request):
        # No verificar autenticación para URLs públicas
        if any(request.path.startswith(url) for url in self.public_urls):
            return self.get_response(request)

        # Verificar token de acceso en cookie
        access_token = request.COOKIES.get('access_token')
        
        if not access_token:
            return JsonResponse({
                'status': 'error',
                'message': 'No autorizado - Token no encontrado'
            }, status=401)

        try:
            # Validar token
            AccessToken(access_token)
            return self.get_response(request)
        except Exception:
            return JsonResponse({
                'status': 'error',
                'message': 'No autorizado - Token inválido'
            }, status=401)

class DisableCSRFForAPI:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/auth/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)