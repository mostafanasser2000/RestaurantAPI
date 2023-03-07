from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255, db_index=True, unique=True)
    
    def __str__(self) -> str:
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f'{self.user.username} Cart'
    
   
    
   
        
class CartItem(models.Model):
     item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='cartitems', unique=True)
     quntity = models.SmallIntegerField()
     unitprice = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
     price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True) 
     cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='items')
     
     def __str__(self) -> str:
         return self.item.title
     
     def save(self, *args, **kwargs):
        self.unitprice = self.item.price
        self.price = self.unitprice * self.quntity
        super(CartItem, self).save(*args, **kwargs)
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # we use related name here as delivery crew and user are both refere to the smame forgien key and django not allowed that
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL,related_name='delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=0)  # order is deliverd or not
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date = models.DateField(db_index=True, auto_now=True)
    
    def __str__(self):
        return self.user.username  
    
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='orderitems')
    quntity = models.SmallIntegerField()
    unitprice = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return self.menuitem.title
  
    class Meta:
        unique_together = ('order', 'menuitem')
