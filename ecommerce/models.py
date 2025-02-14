from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField

import user

# Create your models here.


STOCK_STATUS = (
    ('available', 'Available'),
    ('sold_out', 'Sold-Out')
)

class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/images')
    information = models.TextField()
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    shipping_cost = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.CharField(max_length=200, choices=STOCK_STATUS, default='available')
    favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_products')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')


    @property
    def get_absolute_url(self):
        return self.image.url

    @property
    def get_price(self):
        if self.discount:
            return (self.price * Decimal(1 - self.discount / 100)).quantize(Decimal('0.01'))
        return self.price

    @property
    def rating(self):
        comments = self.comments.all()
        if comments:
            total_rating = (sum([comment.rating for comment in comments]) / self.comments.count()).quantize(Decimal('0.1'))
            return total_rating
        return 5.0

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_attributes', null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True, blank=True)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.SET_NULL, null= True, blank=True)






class ProductComment(models.Model):
    rating = models.DecimalField(validators=[MinValueValidator(0.5), MaxValueValidator(5.0)], max_digits=2, decimal_places=1)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.comment}"


class Customers(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = PhoneNumberField(region="UZ")
    billing_address = models.CharField(max_length=255)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


