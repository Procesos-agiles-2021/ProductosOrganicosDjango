# Generated by Django 3.1.6 on 2021-05-02 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mercadoOrganicosApp', '0002_delete_rol'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producerprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='AdminProfile',
        ),
        migrations.DeleteModel(
            name='ProducerProfile',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
