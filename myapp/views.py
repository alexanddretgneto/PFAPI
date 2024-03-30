from warnings import filters
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrdersSerializer, OrderItemSerializer, GroupSerializer, UserSerializer
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from django.contrib.auth.models import Group, User
from myapp import serializers, models
from myapp.permissions import IsManager, IsDeliveryCrew, IsCustomer, ReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter

# class MenuItemViewSet(viewsets.ModelViewSet):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
class MenuItemViewSet(ModelViewSet):
    permission_classes = [IsAdminUser|IsManager|ReadOnly]
    serializer_class = serializers.MenuItemSerializer
    queryset = models.MenuItem.objects.all()
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category', 'price', 'featured', 'title']
    ordering_fields = ['id', 'price', 'title']
    search_fields = ['category__title', 'title']
    


class GerentePermission(BasePermission):
    def has_permission(self, request, view):
        # Apenas os gerentes têm permissão para realizar todas as operações
        return request.user.groups.filter(name='gerente').exists()

class EntregadorPermission(BasePermission):
    def has_permission(self, request, view):
        # Entregadores podem visualizar os pedidos, mas não podem editar ou excluir nada
        return request.user.groups.filter(name='entregador').exists()

class UserPermission(BasePermission):
    def has_permission(self, request, view):
        # Usuários não cadastrados podem apenas visualizar
        return not request.user.is_authenticated

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, GerentePermission]

    def get_permissions(self):
        if self.action == 'list' and not self.request.user.groups.filter(name='gerente').exists():
            return [permissions.IsAdminUser()]
        return super().get_permissions()

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list' and not self.request.user.groups.filter(name='gerente').exists():
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
class MenuItemPermission(permissions.BasePermission):
    """
    Custom permission to allow only managers to perform CRUD operations,
    allow delivery personnel to list and accept delivery, and allow others to only list.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='gerente').exists():
                return True  # Gerentes têm permissão para CRUD
            elif request.user.groups.filter(name='entregador').exists() and view.action == 'list':
                return True  # Entregadores podem listar
            elif view.action == 'accept_delivery':
                return True  # Adicione outras ações específicas para entregadores aqui
            else:
                return False  # Para todas as outras ações, apenas autenticados podem acessar
        else:
            return view.action == 'list'  # Usuários não autenticados só podem listar




class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class Index(APIView):
    def get(self, request):
        return Response({"message": "Bem-vindo à página inicial do meu aplicativo!"})
