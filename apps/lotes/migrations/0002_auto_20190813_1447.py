# Generated by Django 2.0.13 on 2019-08-13 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lotes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lotes', to='medicamentos.Medicamento', verbose_name='producto del lote*'),
        ),
    ]
