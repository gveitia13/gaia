# Generated by Django 4.1.3 on 2023-01-01 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0008_product_delivery_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suscriptor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo')),
            ],
        ),
    ]