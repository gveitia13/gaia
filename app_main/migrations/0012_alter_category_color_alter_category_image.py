# Generated by Django 4.1.5 on 2023-02-10 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0011_category_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(choices=[('198754', 'Verde'), ('ffc107', 'Amarillo'), ('8cbf44', 'Verde Claro'), ('fd7e14', 'Anaranjado'), ('dc3545', 'Rojo'), ('6c757d', 'Gris'), ('0d6efd', 'Azul')], default='198754', max_length=100, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product/img', verbose_name='Imagen Principal'),
        ),
    ]
