from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Role, UserRole, Permission, RolePermission, Menu
from rest_framework import exceptions  # Importación faltante
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador personalizado para la obtención de tokens JWT.
    Extiende el serializador estándar para incluir datos adicionales del usuario.
    """
    
    @classmethod
    def get_token(cls, user):
        """
        Genera el token con claims personalizados.
        """
        token = super().get_token(user)
        
        # Agrega claims personalizados al token
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        
        # Agrega los roles del usuario al token
        roles = user.user_roles.all().values_list('role__name', flat=True)
        token['roles'] = list(roles)
        
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            data.update({
                'user': {
                    'id': self.user.id,
                    'username': self.user.username,
                    'email': self.user.email,
                    'is_active': self.user.is_active,
                }
            })
            return data
        except exceptions.AuthenticationFailed:
            raise serializers.ValidationError({
            "error": "Credenciales inválidas",
            "code": "invalid_credentials"
        })
        #return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo User de Django.
    Maneja la serialización/deserialización de usuarios.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True}
        }

    def create(self, validated_data):
        """
        Crea y retorna un nuevo usuario con contraseña encriptada.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Role.
    """
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Permission.
    """
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'description', 'created_at']
        read_only_fields = ['created_at']


class UserRoleSerializer(serializers.ModelSerializer):
    """
    Serializador para la relación User-Role.
    Incluye información detallada del rol y del usuario.
    """
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.filter(is_active=True),
        source='role',
        write_only=True
    )
    
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    
    assigned_by = UserSerializer(read_only=True)

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'user_id', 'role', 'role_id', 'assigned_at', 'assigned_by']
        read_only_fields = ['assigned_at', 'assigned_by']


class RolePermissionSerializer(serializers.ModelSerializer):
    """
    Serializador para la relación Role-Permission.
    """
    permission = PermissionSerializer(read_only=True)
    permission_id = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(),
        source='permission',
        write_only=True
    )
    
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.filter(is_active=True),
        source='role',
        write_only=True
    )

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'role_id', 'permission', 'permission_id', 'assigned_at']
        read_only_fields = ['assigned_at']


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Menu.
    Incluye serialización recursiva para submenús.
    """
    children = serializers.SerializerMethodField()
    roles = RoleSerializer(many=True, read_only=True)
    role_ids = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.filter(is_active=True),
        source='roles',
        many=True,
        write_only=True
    )

    class Meta:
        model = Menu
        fields = [
            'id', 'name', 'path', 'component', 'parent', 'icon', 
            'sort_order', 'is_active', 'roles', 'role_ids', 'children',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_children(self, obj):
        """
        Método para obtener recursivamente los submenús.
        """
        children = obj.children.all().order_by('sort_order')
        return MenuSerializer(children, many=True).data


class UserInfoSerializer(serializers.ModelSerializer):
    """
    Serializador para información básica del usuario.
    """
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'last_login', 'roles']
        read_only_fields = fields

    def get_roles(self, obj):
        """
        Obtiene los roles del usuario serializados.
        """
        user_roles = obj.user_roles.filter(role__is_active=True)
        return RoleSerializer([ur.role for ur in user_roles], many=True).data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializador para cambio de contraseña.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )

    def validate_old_password(self, value):
        """
        Valida que la contraseña antigua sea correcta.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta")
        return value

#implementado por sayuri
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return attrs

    def create(self, validated_data):
        # Eliminar password2 del diccionario
        validated_data.pop('password2', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        return user