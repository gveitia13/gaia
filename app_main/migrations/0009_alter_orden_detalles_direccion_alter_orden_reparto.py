# Generated by Django 4.1.5 on 2023-02-08 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0008_product_codigo_alter_generaldata_tropipay_impuesto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='detalles_direccion',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Detalles de dirección'),
        ),
        migrations.AlterField(
            model_name='orden',
            name='reparto',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Reparto'),
        ),
    ]
