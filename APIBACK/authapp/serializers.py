from rest_framework import serializers
from .models import Usuario, ListaDeseos


class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    contraseña = serializers.CharField()

    def validate(self, data):
        correo = data.get("correo")
        password = data.get("password")

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("El usuario no existe.")

        if not usuario.check_password(password):
            raise serializers.ValidationError("Contraseña incorrecta.")

        if not usuario.estado:
            raise serializers.ValidationError("El usuario está inactivo.")

        return usuario
    

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'apellido', 'correo', 'telefono', 'genero', 'rol', 'creado', 'actualizado', 'is_active', 'is_staff']


class ListaDeseosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListaDeseos
        fields = ['name', 'imagen_url', 'price', 'product_url', 'created_at']
