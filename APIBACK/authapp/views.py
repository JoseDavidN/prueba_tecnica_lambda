from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .permissions import IsAdmin
from .serializers import UsuarioSerializer, ListaDeseosSerializer
from django.contrib.auth.hashers import make_password
import requests
from bs4 import BeautifulSoup
from .models import ListaDeseos



class LoginView(APIView):
    def post(self, request):
        email = request.data.get('correo')
        password = request.data.get('password')

        # Verificar si el correo y la contraseña son proporcionados
        if not email or not password:
            return Response({'error': 'Correo y contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        # Intentar autenticar al usuario con correo y contraseña
        try:
            user = get_user_model().objects.get(correo=email)

            # Verificar que la contraseña sea correcta
            if user.check_password(password):
                if user.is_active:  # Verificar si el usuario está activo
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Usuario inactivo. Contacta al administrador.'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)

        except get_user_model().DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class ListUsersView(APIView):
    # Solo los admin pueden acceder
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obtener todos los usuarios
        users = get_user_model().objects.all()

        # Serializar los usuarios
        serializer = UsuarioSerializer(users, many=True)

        # Retornar los usuarios serializados
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)
        

class UserStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, user_id):
        try:
            # Obtén el usuario a actualizar
            user = get_user_model().objects.get(id=user_id)

            # Verifica si el usuario tiene permisos de administrador
            if not request.user.is_staff:
                return Response({"error": "No tiene permisos para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)

            # Cambiar el estado de is_active
            user.is_active = not user.is_active  # Cambia el estado de is_active
            user.save()

            return Response({"message": f"Usuario {'activado' if user.is_active else 'desactivado'} correctamente."}, status=status.HTTP_200_OK)

        except get_user_model().DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)


class CreateUserView(APIView):
    authentication_classes = []  # Deshabilitamos la autenticación
    permission_classes = []  # Hacemos público este endpoint

    def post(self, request):
        data = request.data

        # Validar los campos necesarios
        required_fields = ['nombre', 'apellido', 'correo', 'telefono', 'genero', 'rol', 'password']
        for field in required_fields:
            if field not in data:
                return Response({"error": f"{field} es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el nuevo usuario
        user_data = {
            'nombre': data['nombre'],
            'apellido': data['apellido'],
            'correo': data['correo'],
            'telefono': data['telefono'],
            'genero': data['genero'],
            'rol': 'user',
            # Asegurarse de encriptar la contraseña
            'is_active': True,  # Por defecto el usuario está activo
            # 'is_staff': True if data['rol'] == 'admin' else False,
            'is_staff': False,
        }

        try:
            user = get_user_model().objects.create(**user_data)
            return Response({"message": "Usuario creado correctamente."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user = get_user_model().objects.get(id=user_id)
            serializer = UsuarioSerializer(user)
            return Response(serializer.data)
        except get_user_model().DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        try:
            user = get_user_model().objects.get(id=user_id)
            serializer = UsuarioSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except get_user_model().DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class MercadoLibreSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query')
        if not query:
            return Response({'error': 'El parámetro "query" es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Construir la URL de búsqueda
        search_url = f"https://listado.mercadolibre.com.co/{query}"

        try:
            # Realizar la solicitud HTTP
            response = requests.get(search_url, headers={
                                    "User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                return Response({'error': 'Error al acceder a Mercado Libre.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Analizar el HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            # Selector CSS de los resultados
            items = soup.select('.ui-search-layout__item')

            results = []

            for item in items:
                # Extraer información del producto
                name = item.select_one('.poly-component__title-wrapper').get_text(
                    strip=True) if item.select_one('.poly-component__title') else 'Sin título'
                original_price = item.select_one('.andes-money-amount').get_text(
                    strip=True) if item.select_one('.andes-money-amount__fraction') else 'Sin precio'
                discount_price = item.select_one(
                    '.poly-price__current .andes-money-amount__fraction').get_text(strip=True) if item.select_one('.poly-price__current .andes-money-amount__fraction') else 'Sin precio'
                discount_percentage = item.select_one(
                    '.poly-price__current .andes-money-amount__discount').get_text(strip=True) if item.select_one('.poly-price__current .andes-money-amount__discount') else 'Sin descuento'
                link = item.select_one(
                    'a.poly-component__title')['href'] if item.select_one('a.poly-component__title') else '#'
                name_seller = item.select_one(
                    '.poly-component__brand').get_text(strip=True) if item.select_one('.poly-component__brand') else 'Sin vendedor'
                rating = item.select_one('span.poly-reviews__rating').get_text(
                    strip=True) if item.select_one('span.poly-reviews__rating') else 'Sin rating'
                image_url = item.select_one(
                    'img.poly-component__picture')['src'] if item.select_one('img.poly-component__picture') else '#'

                results.append({
                    'name': name,
                    'original_price': original_price,
                    'discount_price': discount_price,
                    'discount_percentage': discount_percentage,
                    'seller': {
                        'name': name_seller,
                    },
                    'rating': rating,
                    'image_url': image_url,
                    'product_url': link
                })

            return Response({
                'search_term': query,
                'results': results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddItemList(APIView):
    permission_classes = [IsAuthenticated]  # Hacemos público este endpoint

    def post(self, request):
        data = request.data

        print(data)

        # Crear el nuevo ítem
        item_data = {
            'name': data['name'],
            'imagen_url': data['imagen'],
            'price': data['price'],
            'product_url': data['product_url'],
        }

        try:
            item = ListaDeseos.objects.create(**item_data)
            return Response({"message": "Producto agregado correctamente."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = ListaDeseos.objects.all()
        serializer = ListaDeseosSerializer(items, many=True)
        return Response(serializer.data)
