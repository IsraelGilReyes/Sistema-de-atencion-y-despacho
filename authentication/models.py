from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    """
    Modelo para gestionar los diferentes roles de usuario en el sistema.
    Ejemplos típicos: 'Administrador', 'Supervisor', 'Usuario Regular', etc.
    
    Métodos:
    - __str__: Representación legible para humanos (devuelve el nombre del rol)
    
    Config Meta:
    - verbose_name: Nombre singular para el admin
    - verbose_name_plural: Nombre plural para el admin
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
    Modelo para permisos específicos del sistema que pueden asignarse a roles.
    Define acciones concretas como 'crear_usuario', 'editar_reporte', etc.
    
    
    
    Este modelo permite un control granular sobre las acciones en el sistema.
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
    Modelo puente que relaciona usuarios con roles (relación muchos-a-muchos).
    Registra qué rol(es) tiene asignado cada usuario y quién se los asignó.
    

    Config Meta:
    - unique_together: Evita duplicados en la relación usuario-rol
    - verbose_name: Nombre legible para el admin
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
    Modelo puente que asocia permisos específicos a roles.
    Define qué acciones puede realizar cada tipo de rol.
    
    Config Meta:
    - unique_together: Previene asignaciones duplicadas del mismo permiso a un rol
    - verbose_name: Nombre legible para interfaces administrativas
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
    Modelo para menús dinámicos en la interfaz, con control de acceso por roles.
    Permite construir estructuras jerárquicas de navegación (menús con submenús).
    
    Este modelo es especialmente útil para aplicaciones con:
    - Interfaces dinámicas basadas en roles
    - Estructuras de navegación complejas
    - Control granular de acceso a secciones
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