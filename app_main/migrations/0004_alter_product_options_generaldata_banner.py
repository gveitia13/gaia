# Generated by Django 4.1.3 on 2022-12-20 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0003_product_is_important'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AddField(
            model_name='generaldata',
            name='banner',
            field=models.ImageField(null=True, upload_to='datos_generales/banner', verbose_name='Banner'),
        ),
    ]
