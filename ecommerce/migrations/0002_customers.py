# Generated by Django 5.1.5 on 2025-02-04 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('billing_address', models.CharField(max_length=255)),
                ('joined', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
