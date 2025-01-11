from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, correo, contraseña=None, **extra_fields):
        """
        Crea y guarda un usuario con correo y contraseña.
        """
        if not correo:
            raise ValueError('El correo debe ser proporcionado')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(contraseña)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con correo y contraseña.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('user', 'Usuario'),
    ]

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    # El campo is_active ya está incluido en AbstractBaseUser y se usa para activar/desactivar cuentas
    is_active = models.BooleanField(default=True)
    # Para indicar si el usuario tiene permisos de administración
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo'  # Especificamos que el correo será el campo de autenticación
    # Campos requeridos para crear un superusuario
    REQUIRED_FIELDS = ['nombre', 'apellido']

    # Relaciones con grupos y permisos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Cambiamos el nombre para evitar conflictos
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        # Cambiamos el nombre para evitar conflictos
        related_name='usuario_permissions_set',
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol}"


class ListaDeseos(models.Model):
    name = models.CharField(max_length=255)
    imagen_url = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
