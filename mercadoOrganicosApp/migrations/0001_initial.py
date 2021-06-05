# Generated by Django 3.2.4 on 2021-06-05 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'carritos',
            },
        ),
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(verbose_name='Fecha de creacion')),
                ('admin_creador', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Catalogos',
            },
        ),
        migrations.CreateModel(
            name='ItemCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagenUrl', models.CharField(max_length=500)),
                ('visibilidad', models.BooleanField()),
                ('catalogo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mercadoOrganicosApp.catalogo')),
            ],
            options={
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.FloatField()),
                ('itemId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mercadoOrganicosApp.itemcompra')),
            ],
            options={
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_compra', models.DateTimeField(verbose_name='Fecha de compra')),
                ('fecha_entrega', models.DateTimeField(verbose_name='Fecha de entrega')),
                ('direccion_entrega', models.CharField(max_length=400)),
                ('metodo_pago', models.CharField(max_length=200)),
                ('numero_tarjeta', models.CharField(max_length=200)),
                ('numero_cuota', models.IntegerField()),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mercadoOrganicosApp.carrito')),
            ],
            options={
                'verbose_name_plural': 'Ordenes',
            },
        ),
        migrations.CreateModel(
            name='ItemCompraCarrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mercadoOrganicosApp.carrito')),
                ('item_compra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mercadoOrganicosApp.itemcompra')),
            ],
            options={
                'verbose_name_plural': 'ItemsCompraCarrito',
            },
        ),
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='carrito',
            name='item_compras',
            field=models.ManyToManyField(through='mercadoOrganicosApp.ItemCompraCarrito', to='mercadoOrganicosApp.ItemCompra'),
        ),
        migrations.AddField(
            model_name='carrito',
            name='usuario_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
