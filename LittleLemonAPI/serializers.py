from rest_framework import serializers
from .models import Cart, Category, MenuItem, Order, OrderItem, User, CartItem
import bleach
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=255)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class CustomSerializer(serializers.Serializer):
   
    # user_id = serializers.ReadOnlyField(source='user.id')
    
    def validate(self, attrs):
        attrs['username'] = bleach.clean(attrs['username'])
        attrs['email'] = bleach.clean(attrs['email'])
        return super().validate(attrs)

       
# category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

  
    def validate(self, attrs):
        # sanitize data
        attrs['title'] = bleach.clean(attrs['title'])
        return super().validate(attrs)    
    
# Menu Item serializer    
class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category',read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_name']

           
    def validate(self, attrs):
        if(attrs['price'] <= 0):
            raise serializers.ValidationError('Price should be greater than 0') 
        # sanitize data   
        attrs['title'] = bleach.clean(attrs['title'])
        return super().validate(attrs)

# cart item serializer
class CartItemSerializer(serializers.ModelSerializer): 
    item_name = serializers.StringRelatedField(source='item', read_only=True)
    class Meta:
        model = CartItem
        fields = ('id','cart','item', 'item_name', 'quntity', 'unitprice', 'price')
        extra_kwargs = {
            'quntity': {'min_value': 0},
            'unitprice': {'read_only': True},
            'price': {'read_only': True},
            'cart': {'read_only': True}
        }
        
        
       
# cart serializer
class CartSerializer(serializers.ModelSerializer): 
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name='calc_total', read_only='True')
    class Meta:
        model = Cart
        fields = ['id','items', 'total']

    def calc_total(self, cart:Cart):
        items = cart.items.all()
        total = sum([item.price for item in items])
        return total
    
class OrderItemSerialzer(serializers.ModelSerializer):
    item_name = serializers.StringRelatedField(source='menuitem',many=False)
    class Meta:
        model = OrderItem
        fields = ('id','order', 'menuitem', 'item_name', 'quntity', 'unitprice', 'price')
        
        extra_kwargs = {
            'quntity': {'min_value': 0},
            'unitprice': {'read_only': True},
            'price': {'read_only': True},
            'order': {'read_only': True}
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerialzer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name='calc_total', read_only=True)
    delivery_crew_name = serializers.StringRelatedField(source='delivery_crew', read_only=True)
    status_detail = serializers.SerializerMethodField(method_name='get_status', read_only=True) 
    class Meta:
        model = Order
        fields = ['id', 'items', 'total', 'date', 'status','status_detail', 'delivery_crew', 'delivery_crew_name']

    extra_kwargs = {
            'date': {'read_only': True},
        }
        
    def calc_total(self, order:Order):
        order_items = order.items.all()
        if order_items:
            return sum([item.price for item in order_items])
        return 0
    
    def get_status(self, order:Order):
        if order.status:
            return "Delivered"
        return "Not delivered yet"

