from django.urls import path, include
from rest_framework import routers
from .views import GerentePermission, Index, CategoryViewSet, MenuItemViewSet, CartViewSet, OrderViewSet, OrderItemViewSet
from myapp.views import UserViewSet, GroupViewSet

# Crie um roteador
router = routers.DefaultRouter()
# Registre as visualizações do roteador
router.register(r'categories', CategoryViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'carts', CartViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
# Condicionalmente registre os viewsets de User e Group
# if GerentePermission:


app_name = 'myapp'
urlpatterns = [
    path('', include(router.urls)),
    path('index/', Index.as_view(), name='index'),
]