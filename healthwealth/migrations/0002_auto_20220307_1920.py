# Generated by Django 3.1.8 on 2022-03-07 12:20

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthwealth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_url',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
