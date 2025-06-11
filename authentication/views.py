from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import Role, UserRole
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    RoleSerializer,
    UserRoleSerializer,
    UserInfoSerializer,
    RegisterSerializer #sayuri
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta


User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                # Configurar cookies HttpOnly
                access_token = response.data['access']
                refresh_token = response.data['refresh']
                
                response.set_cookie(
                    'access_token',
                    access_token,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    max_age=3600  # 1 hora
                )
                
                response.set_cookie(
                    'refresh_token',
                    refresh_token,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    max_age=24 * 3600  # 24 horas
                )
                
                # Eliminar tokens de la respuesta JSON para mayor seguridad
                response.data = {
                    'status': 'success',
                    'user': response.data.get('user', {}),
                    'message': 'Login exitoso'
                }
            return response
        #login fallido 
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Credenciales inválidas',
                'detail': str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)

# Vista de Registro
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data) #toma los datos del usuario
    
    if serializer.is_valid():
        try:
            # Crear el usuario
            user = serializer.save()
            
            # Generar tokens JWT para login automático
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Preparar la respuesta
            response = Response({
                'status': 'success',
                'message': 'Usuario registrado exitosamente',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
            
            # Configurar cookies HttpOnly
            response.set_cookie(
                'access_token',
                access_token,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=3600  # 1 hora access token
            )
            
            response.set_cookie(
                'refresh_token',
                refresh_token,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=24 * 3600  # 24 horas refresh token
            )
            
            return response
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Error al registrar el usuario',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'status': 'error',
        'message': 'Error en el registro',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

# Vista de Logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Obtener el token de refresco de la cookie
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
        response = Response({
            'status': 'success',
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
        
        # Eliminar las cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
    except Exception:
        return Response({
            'status': 'error',
            'message': 'Error al cerrar sesión'
        }, status=status.HTTP_400_BAD_REQUEST)

# Vista para listar roles en donde hay ACCESO RESTRINGIDO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def role_list(request):
    roles = Role.objects.filter(is_active=True)
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)

# Vista para crear roles
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_role(request):
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para obtener roles del usuario
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_roles(request):
    user_roles = UserRole.objects.filter(user=request.user, role__is_active=True)
    serializer = UserRoleSerializer(user_roles, many=True)
    return Response(serializer.data)

# Vista para asignar roles
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_role(request):
    data = {
        'user_id': request.data.get('user_id'),
        'role_id': request.data.get('role_id'),
        'assigned_by': request.user.id
    }
    serializer = UserRoleSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para información del usuario actual
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    serializer = UserInfoSerializer(request.user)
    return Response({
        'status': 'success',
        'user': serializer.data
    })

# Vista para listar usuarios
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Vista para crear usuarios (admin)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)