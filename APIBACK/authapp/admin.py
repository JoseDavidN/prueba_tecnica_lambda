from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ['nombre', 'apellido', 'correo',
                    'rol', 'is_active', 'is_staff']
    search_fields = ['correo']
    ordering = ['correo']
    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Información Personal', {
        'fields': ('nombre', 'apellido', 'telefono', 'genero', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Fechas', {'fields': ('creado', 'actualizado')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'password1', 'password2', 'nombre', 'apellido', 'rol')}
        ),
    )

    exclude = ('creado', 'actualizado')

    readonly_fields = ('creado', 'actualizado')


admin.site.register(Usuario, UsuarioAdmin)
