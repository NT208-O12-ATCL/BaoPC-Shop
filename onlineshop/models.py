from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.CharField(max_length=255)
    image = models.ImageField(null=True)
    category = models.CharField(max_length=255)
    purchase_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class EmailAddress(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    order_details = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Order #{self.pk} - {self.name}'
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.name} on {self.product.name}'
    
    