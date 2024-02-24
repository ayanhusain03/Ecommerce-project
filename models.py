from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Subcategories(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    desc =  models.TextField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    subcategories = models.ForeignKey(Subcategories, on_delete=models.CASCADE)
    price = models.IntegerField()
    image = models.ImageField(upload_to="product_images")
    objects = models.Manager()

    def __str__(self):
        return self.product_name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Order(models.Model):
    order_id = models.IntegerField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default= 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)