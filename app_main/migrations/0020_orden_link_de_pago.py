# Generated by Django 4.1.3 on 2023-01-23 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0019_orden_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='link_de_pago',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]