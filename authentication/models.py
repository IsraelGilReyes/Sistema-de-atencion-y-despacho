from django.db import models
from django.contrib.auth.models import User

class Role(models.Model): 
    """
    TABLA DE ROLES-Modelo para roles de usuario (ej: admin, super, usuario)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

class Permission(models.Model):
    """
    TABLA DE PERMISOS-Modelo para permisos específicos (ej: crear_usuario, ver_reportes)
    """
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'

class UserRole(models.Model):
    """
    TABLA DE RELACION usuario/rolModelo para asignar roles a usuarios
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='role_assignments')

    class Meta:
        unique_together = ('user', 'role')
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuario'

class RolePermission(models.Model):
    """
    Modelo para asignar permisos a roles
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('role', 'permission')
        verbose_name = 'Permiso de Rol'
        verbose_name_plural = 'Permisos de Roles'

class Menu(models.Model):
    """
    TABLA DE MENUS-Modelo para menús dinámicos
    """
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    component = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.CharField(max_length=50, null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    roles = models.ManyToManyField(Role, related_name='menus')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Menú'
        verbose_name_plural = 'Menús'
        ordering = ['sort_order', 'name']
