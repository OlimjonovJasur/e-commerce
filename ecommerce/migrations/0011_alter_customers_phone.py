# Generated by Django 5.1.5 on 2025-02-05 21:38

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_alter_productcomment_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='UZ'),
        ),
    ]
