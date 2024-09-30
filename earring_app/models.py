from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    username = models.CharField(max_length=150,unique=True)
    name=models.CharField(max_length=45)
    email = models.EmailField(max_length=255, unique=True)
    phone=models.CharField(max_length=45,unique=True)
    password=models.CharField(max_length=40)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


    def __str__(self):
        return self.name
    from django.db import models
from django.contrib.auth.models import User

class Supplier(models.Model):
    
    name = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=255, unique=True,null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.TextField(null=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
 
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images', blank=True)
    quantity = models.IntegerField(default=0)
    manufacture = models.CharField(max_length=100, default="Gokuldas Gangwani")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User
from django.db import models

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.user.username
class Orders(models.Model):
    total=models.DecimalField(max_digits=10, decimal_places=2)
    user=models.CharField(max_length=255)
    date = models.CharField(max_length=200,default='not set')
    time = models.CharField(max_length=200,default='not set')
    status = models.CharField(default='pending',max_length=200)
    fname = models.CharField(max_length=100,default='not set')
    lname = models.CharField(max_length=100,default='not set')
    address = models.CharField(max_length=250,default='not set')
    contact = models.CharField(max_length=100,default='not set')
    sstatus = models.CharField(max_length=20,default='not set')


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.CharField(max_length=255)
    date_added = models.CharField(max_length=200)
    status = models.CharField(default='carted',max_length=200)
    orderid = models.CharField(max_length=100,default='not set')
    price=models.DecimalField(max_digits=10, decimal_places=2,default=0)
 
    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    


    
class SupplyRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'


