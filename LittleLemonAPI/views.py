from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes, APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters, status
from .serializers import *
from .models import *
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.reverse import reverse
import pdb
# Create your views here.


# root end point
@api_view()
def api_root(request):
    return Response({
        'token-login': 'http://127.0.0.1:8000/auth/token/login/',
        'users': reverse('user-list', request=request, format=None),
        'menu-items': reverse('item-list', request=request, format=None),
        'categories': reverse('category-list', request=request, format=None),
        'managers': reverse('manager-list', request=request, format=None),
        'delivery-crew': reverse('delivery-crew-list', request=request, format=None),
        'cart': 'http://127.0.0.1:8000/api/cart/menu-items/',
        'orders': 'http://127.0.0.1:8000/api/orders/',
        
    })

#  categories end point
class CategoryiesView(generics.ListCreateAPIView):
    """List all catgories or create new categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission, IsAuthenticated]


# menu item list  end point
class  MenuItemListView(generics.ListCreateAPIView):
    """List all menu items, and creat new one"""
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [MenuItemPermission, IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['price']
    
# menu item detail end point
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
     """Retrive or update or delete menu item"""
     queryset = MenuItem.objects.all()
     serializer_class = MenuItemSerializer
     permission_classes = [MenuItemPermission, IsAuthenticated]



class ManagerGroupListView(generics.ListCreateAPIView):
    """List all managers and new users to managers"""
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data['email'], username=serializer.validated_data['username'])
        manager_group = Group.objects.get(name='Manager')
        if manager_group.user_set.contains(user):
            return Response({'user already exist in manager group'})
        self.perform_create(serializer,user_id=user.id, group=manager_group)
        return Response({'user is added to Manager Group'}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer,*args,**kwargs):
        kwargs['group'].user_set.add(kwargs['user_id'])
    
    
class ManagerGroupDetailView(generics.RetrieveDestroyAPIView):
    """Retrive, update or delete manager"""
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        manger_group = Group.objects.get(name='Manager')
        if manger_group.user_set.contains(user):
            return Response(serializer.data)
        return Response({'User not in the manager group to be deleted'}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = get_object_or_404(User, username=instance)
        self.perform_destroy(user)
        return Response({'User has been removed from manager group'}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        manager_group = Group.objects.get(name='Manager')
        manager_group.user_set.remove(instance)
    

class DeliveryCrewListView(generics.ListCreateAPIView):
    """List all delivery crew and users to delivery crew"""
    queryset = User.objects.filter(groups__name='Delivery')
    serializer_class = UserSerializer
    permission_classes = [ManagerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.validated_data['username'], email=serializer.validated_data['email'])
        delivery_group = Group.objects.get(name='Delivery')
        if delivery_group.user_set.contains(user):
            return Response({'User is already in delivery crew'})
        self.perform_create(serializer, user_id=user.id, group=delivery_group)
        return Response({'User is add to delivery crew'}, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer, *args, **kwargs):
        kwargs['group'].user_set.add(kwargs['user_id'])

class DeliveryCrewDetailView(generics.RetrieveDestroyAPIView):
    """Retrive, update and delete user from delivery crew"""
    queryset = User.objects.all()
    permission_classes = [ManagerPermission]
    serializer_class = UserSerializer
 
    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset,pk=pk)
        serializer = UserSerializer(user)
        delivery_group = Group.objects.get(name='Delivery')
        if delivery_group.user_set.contains(user):
            return Response(serializer.data)
        return Response({'User not exist in delivery crew'}, status=status.HTTP_404_NOT_FOUND)
        
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = User.objects.get(username=instance)
        self.perform_destroy(user)
        return Response({'User has been deleted form delivery crew'}, status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        delivery_group = Group.objects.get(name='Delivery')
        delivery_group.user_set.remove(instance)


   
# cart end point
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([CartPermission, IsAuthenticated])
def cart_view(request):
   """List cart items for specific user, add new items, delete items"""
   cart = None
   
   # if it's first time for user to call end point create empty cart
   try:
       cart = Cart.objects.get(user=request.user)
   except Cart.DoesNotExist:
        cart = Cart(user=request.user)
        cart.save()
        
   if request.method == 'GET':
       
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
   if request.method == 'POST':
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   if request.method == 'DELETE':
       items = CartItem.objects.filter(cart__id=cart.id)
       items.delete()
       return Response({'All items are deleted'},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list(request):
    """List all orders, and create new ones"""
    orders = Order.objects.all()
    
    # GET
    if request.method == 'GET':
        # get all orders for manager
        if request.user.groups.filter(name='Manager').exists():
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data)
        # return all delivery assigned orders
        elif request.user.groups.filter(name='Delivery'):
             
             serializer = OrderSerializer(orders.filter(delivery_crew=request.user), many=True)
             return Response(serializer.data)
         # return orders for customer
        order = orders.filter(user=request.user) 
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        if (request.user.groups.filter(name='Manager')) or request.user.groups.filter(name='Delivery'):
            return Response({'only customers can make orders'},status=status.HTTP_403_FORBIDDEN)
        
        # check if customer have items on cart and create order for those items
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        if cart_items:
            order = Order(user=request.user)  # crate an order for that user
            order.save() # save that order
            
            for c_item in cart_items:  # create order items from cart 
                order_item = OrderItem(order=order,menuitem=c_item.item, quntity=c_item.quntity, unitprice=c_item.unitprice, price=c_item.price)
                order_item.save()
            cart_items.delete()  # flush cart
            serializer = OrderSerializer(order)
            return Response(serializer.data) 
         
        return Response({'your cart is empty, Please put items in your cart first to make and order'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def order_deatil(request, pk):
    """Retrive, update and delete orders"""
    order = Order.objects.get(pk=pk)
    
    if request.method == 'GET':
        # check who made the request
         if request.user.groups.filter(name='Manager').exists():
             serializer = OrderSerializer(order)
             return Response(serializer.data, 200)
         
         elif request.user.groups.filter(name='Delivery').exists():
             if order.delivery_crew == request.user:
                serializer = OrderSerializer(order)
                return Response(serializer.data, 200)
             return Response({"This order is not assigned to you"}, status=status.HTTP_401_UNAUTHORIZED)
        
         elif order.user == request.user:
            serializer = OrderSerializer(order)
            return Response(serializer.data, 200)
        
         return Response(status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'PUT':
        if request.user.groups.filter(name='Manager').exists():
            delivery = User.objects.get(pk=request.data.get('delivery_crew'))
            
            if not(Group.objects.get(name='Delivery').user_set.contains(delivery)):
                return Response("The assigned user not form delivery crew", 400)
            
            serializer = OrderSerializer(order,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 200)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'PATCH':
        if request.user.groups.filter(name='Manager').exists():
            delivery = User.objects.get(pk=request.data.get('delivery_crew'))
            
            if not(Group.objects.get(name='Delivery').user_set.contains(delivery)):
                return Response("The assigned user not form delivery crew", 400)
            
            serializer = OrderSerializer(order,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 200)
            
        elif request.user.groups.filter(name='Delivery').exists():
             if request.data.get('delivery_crew'):
                 return Response('only managers can assign delivery crew to orders', status=status.HTTP_403_FORBIDDEN)
             serializer = OrderSerializer(order,data=request.data)
             if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 200)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'DELETE':
        if request.user.groups.filter(name='Manager').exists():
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
       
             
    
    
    
  