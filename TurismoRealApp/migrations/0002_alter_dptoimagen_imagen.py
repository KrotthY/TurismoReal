# Generated by Django 4.1.3 on 2023-09-13 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TurismoRealApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dptoimagen',
            name='imagen',
            field=models.ImageField(null=True, upload_to='dpto_imagenes/'),
        ),
    ]
