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
    UserInfoSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

# Vista de Login con serializador personalizado
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Vista de Registro
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista de Logout
@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Vista para listar roles
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
    return Response(serializer.data)

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