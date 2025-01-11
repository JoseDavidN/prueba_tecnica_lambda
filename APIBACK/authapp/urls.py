# authapp/urls.py
from django.urls import path
from .views import LoginView, ListUsersView, UserStatusUpdateView, CreateUserView, UserDetailView, MercadoLibreSearchView, AddItemList, UserWishlistView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),  # Ruta para el login
    path('users/', ListUsersView.as_view(), name='list-users'),
    path('users/<int:user_id>/status/', UserStatusUpdateView.as_view(), name='user-status-update'),
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('search/', MercadoLibreSearchView.as_view(), name='mercadolibre_search'),
    path('wishlist/', AddItemList.as_view(), name='wishlist'),
    path('wishlistview/', UserWishlistView.as_view(), name='wishlistview'),
]
