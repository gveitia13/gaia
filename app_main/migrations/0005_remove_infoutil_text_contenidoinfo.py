# Generated by Django 4.1.3 on 2023-01-27 05:25

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_main', '0004_alter_componenteorden_options_alter_orden_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infoutil',
            name='text',
        ),
        migrations.CreateModel(
            name='ContenidoInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Contenido')),
                ('image', models.ImageField(blank=True, null=True, upload_to='info/', verbose_name='Imagen')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_main.infoutil')),
            ],
        ),
    ]