from django.db import models

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
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    order_details = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Order #{self.pk} - {self.name}'
    