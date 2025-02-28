from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, ProductComment, Customers
from decimal import Decimal

def calculate_product_rating(product):
    comments = product.comments.all()
    if comments:
        total_rating = (sum([comment.rating for comment in comments]) / product.comments.count()).quantize(Decimal('0.1'))
        return total_rating
    return 5.0

@receiver(post_save, sender=Product)
def product_saved(sender, instance, **kwargs):
    print(f'Product "{instance.name}" has been saved.')

@receiver(post_save, sender=ProductComment)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    product_rating = calculate_product_rating(product)
    print(f'Updated rating for "{product.name}": {product_rating}')

@receiver(post_delete, sender=ProductComment)
def delete_comment_update_rating(sender, instance, **kwargs):
    product = instance.product
    product_rating = calculate_product_rating(product)
    print(f'Updated rating after deletion for "{product.name}": {product_rating}')

@receiver(post_save, sender=Customers)
def customer_created(sender, instance, created, **kwargs):
    if created:
        print(f'New customer "{instance.name}" has been added.')