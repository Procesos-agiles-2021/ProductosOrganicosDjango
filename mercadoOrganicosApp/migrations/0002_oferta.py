# Generated by Django 2.2 on 2021-05-31 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mercadoOrganicosApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidadRestante', models.IntegerField()),
                ('precioUnidad', models.FloatField()),
                ('productoId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mercadoOrganicosApp.Producto')),
            ],
        ),
    ]
