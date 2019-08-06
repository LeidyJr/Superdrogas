# Generated by Django 2.0.13 on 2019-08-05 08:05

import apps.empresas.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='direccion',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='dirección del negocio*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='email',
            field=models.EmailField(default='aaa', max_length=254, verbose_name='correo electrónico del negocio*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='eslogan',
            field=models.CharField(default='sss', max_length=100, verbose_name='eslogan de su negocio*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='logo',
            field=models.ImageField(default=1, upload_to=apps.empresas.models.crear_ruta_logo, verbose_name='logo del negocio*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='sobre_nosotros',
            field=models.TextField(default='kkk', verbose_name='sobre nosotros (descripción de su negocio)*'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresa',
            name='telefono',
            field=models.CharField(default=1, max_length=100, verbose_name='teléfono del negocio*'),
            preserve_default=False,
        ),
    ]
