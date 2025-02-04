from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


STOCK_STATUS = (
    ('available', 'Available'),
    ('sold_out', 'Sold-Out')
)

class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/images')
    information = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    shipping_cost = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.CharField(max_length=200, choices=STOCK_STATUS, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Customers(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    billing_address = models.CharField(max_length=255)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email


