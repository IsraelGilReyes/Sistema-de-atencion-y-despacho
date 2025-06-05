# Importaciones de Django REST Framework para manejar peticiones HTTP y respuestas
from rest_framework import status  # Códigos de estado HTTP (200, 401, etc.)
from rest_framework.decorators import api_view, permission_classes  # Decoradores para vistas API
from rest_framework.response import Response  # Clase para construir respuestas HTTP estandarizadas
from rest_framework.permissions import AllowAny  # Permiso que permite acceso sin autenticación

# Importaciones para JWT (JSON Web Tokens)
from rest_framework_simplejwt.tokens import RefreshToken  # Para generar tokens de acceso/refresh

# Importación de Django para autenticación de usuarios
from django.contrib.auth import authenticate  # Función para validar credenciales de usuario


# Vista para el login de usuarios
@api_view(['POST'])  # Decorador que especifica que esta vista solo acepta métodos POST
@permission_classes([AllowAny])  # Permite que cualquier usuario acceda (sin necesidad de estar autenticado)
def login(request):
    """
    Endpoint para autenticación de usuarios.
    Recibe username y password, devuelve tokens JWT si las credenciales son válidas.
    """
    # Extrae username y password del cuerpo de la petición (request.data)
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Autentica al usuario con las credenciales proporcionadas
    user = authenticate(username=username, password=password)
    
    if user is not None:  # Si la autenticación fue exitosa
        # Genera tokens JWT para el usuario
        refresh = RefreshToken.for_user(user)
        
        # Construye la respuesta con:
        # - Token de acceso (para autenticar peticiones)
        # - Token de refresh (para obtener nuevos tokens)
        # - Datos básicos del usuario
        return Response({
            'token': str(refresh.access_token),  # Token de acceso
            'refresh': str(refresh),  # Token de refresh
            'user': {  # Información del usuario
                'username': user.username,
                'email': user.email,
                'id': user.id
            }
        })
    else:
        # Si las credenciales son inválidas, devuelve error 401 (No autorizado)
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


# Vista para el logout de usuarios
@api_view(['POST'])  # Solo acepta método POST
def logout(request):
    """
    Endpoint para invalidar tokens JWT (logout).
    Recibe un token refresh y lo añade a la lista negra.
    """
    try:
        # Extrae el token refresh del cuerpo de la petición
        refresh_token = request.data["refresh"]
        
        # Crea un objeto RefreshToken y lo invalida (blacklist)
        token = RefreshToken(refresh_token)
        token.blacklist()  # Añade el token a la lista negra
        
        # Devuelve código 205 (Reset Content) indicando éxito
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        # Si hay algún error (ej: token inválido), devuelve 400 (Bad Request)
        return Response(status=status.HTTP_400_BAD_REQUEST)