# Generated by Django 2.0.13 on 2019-08-10 00:19

import apps.medicamentos.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categorias', '0003_auto_20190809_0005'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalMedicamento',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('nombre', models.CharField(db_index=True, max_length=50, verbose_name='nombre del producto*')),
                ('unidad_medida', models.CharField(max_length=50, verbose_name='unidad de medida*')),
                ('precio', models.PositiveIntegerField(verbose_name='precio de venta*')),
                ('cantidad', models.PositiveIntegerField(verbose_name='cantidad actual*')),
                ('descripcion', models.TextField(blank=True, verbose_name='descripción')),
                ('imagen', models.TextField(blank=True, max_length=100, verbose_name='imagen del producto')),
                ('activo', models.BooleanField(default=True, verbose_name='¿El producto está activo actualmente?')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('categoria', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='categorias.Categoria')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical medicamento',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='nombre del producto*')),
                ('unidad_medida', models.CharField(max_length=50, verbose_name='unidad de medida*')),
                ('precio', models.PositiveIntegerField(verbose_name='precio de venta*')),
                ('cantidad', models.PositiveIntegerField(verbose_name='cantidad actual*')),
                ('descripcion', models.TextField(blank=True, verbose_name='descripción')),
                ('imagen', models.ImageField(blank=True, upload_to=apps.medicamentos.models.crear_ruta_medicamento, verbose_name='imagen del producto')),
                ('activo', models.BooleanField(default=True, verbose_name='¿El producto está activo actualmente?')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='categorias.Categoria', verbose_name='categoría del producto*')),
            ],
            options={
                'ordering': ['nombre'],
                'permissions': (('gestionar_productos', 'Gestión de productos'),),
            },
        ),
    ]
