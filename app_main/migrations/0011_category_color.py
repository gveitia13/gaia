# Generated by Django 4.1.5 on 2023-02-10 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0010_alter_orden_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(choices=[('success', 'Verde'), ('warning', 'Amarillo'), ('semi-success', 'Verde Claro'), ('orange', 'Anaranjado'), ('danger', 'Rojo'), ('secondary', 'Gris'), ('primary', 'Azul')], default='success', max_length=100, verbose_name='Color'),
        ),
    ]