# Importaciones de Django REST Framework para manejar peticiones HTTP y respuestas
from rest_framework import status  # Códigos de estado HTTP (200, 401, etc.)
from rest_framework.decorators import api_view, permission_classes  # Decoradores para vistas API
from rest_framework.response import Response  # Clase para construir respuestas HTTP estandarizadas
from rest_framework.permissions import AllowAny, IsAuthenticated  # Permiso que permite acceso sin autenticación y permiso que requiere autenticación
# Importaciones para JWT (JSON Web Tokens)
from rest_framework_simplejwt.tokens import RefreshToken  # Para generar tokens de acceso/refresh
# Importación de Django para autenticación de usuarios
from django.contrib.auth import authenticate, get_user_model # Función para validar credenciales de usuario
from .models import Role, UserRole
User = get_user_model()


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

# Vista para el registro de nuevos usuarios
@api_view(['POST'])
def register(request):
    """
    Crear un nuevo usuario
    """
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
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
    

# Vista para obtener la lista de roles
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def role_list(request):
    """
    Obtener lista de roles
    """
    roles = Role.objects.filter(is_active=True)
    data = [{
        'id': role.id,
        'name': role.name,
        'description': role.description,
        'created_at': role.created_at
    } for role in roles]
    return Response(data)

# Vista para crear un nuevo rol
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_role(request):
    """
    Crear un nuevo rol
    """
    name = request.data.get('name')
    description = request.data.get('description')

    if Role.objects.filter(name=name).exists():
        return Response(
            {'error': 'Ya existe un rol con ese nombre'},
            status=status.HTTP_400_BAD_REQUEST
        )

    role = Role.objects.create(
        name=name,
        description=description
    )

    return Response({
        'id': role.id,
        'name': role.name,
        'description': role.description,
        'created_at': role.created_at
    }, status=status.HTTP_201_CREATED)

# Vista para obtener los roles asignados al usuario actual
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_roles(request):
    """
    Obtener roles del usuario actual
    """
    user_roles = UserRole.objects.filter(user=request.user, role__is_active=True)
    data = [{
        'id': user_role.role.id,
        'name': user_role.role.name,
        'description': user_role.role.description,
        'assigned_at': user_role.assigned_at
    } for user_role in user_roles]
    return Response(data)

# Vista para asignar un rol a un usuario
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_role(request):
    """
    Asignar rol a un usuario
    """
    user_id = request.data.get('user_id')
    role_id = request.data.get('role_id')

    try:
        role = Role.objects.get(id=role_id, is_active=True)
        user_role = UserRole.objects.create(
            user_id=user_id,
            role=role,
            assigned_by=request.user
        )
        return Response({
            'message': 'Rol asignado correctamente',
            'assigned_at': user_role.assigned_at
        })
    except Role.DoesNotExist:
        return Response(
            {'error': 'El rol no existe o no está activo'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        ) 
    

###########################################################3

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """
    Se debe obtener la información del usuario actual
    """
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'last_login': user.last_login
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    """
    Obtener lista de usuarios
    """
    users = User.objects.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'last_login': user.last_login
        })
    return Response(user_list)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    """
    Crear un nuevo usuario
    """
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        ) 