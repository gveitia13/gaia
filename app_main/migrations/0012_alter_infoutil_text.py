# Generated by Django 4.1.3 on 2023-01-06 09:53

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0011_alter_infoutil_options_remove_infoutil_gnd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infoutil',
            name='text',
            field=ckeditor.fields.RichTextField(verbose_name='Contenido'),
        ),
    ]
