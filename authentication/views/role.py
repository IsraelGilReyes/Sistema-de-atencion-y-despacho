from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Role, UserRole

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