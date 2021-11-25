# Generated by Django 3.1.8 on 2021-11-23 06:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('healthwealth', '0005_documentaccess'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentaccess',
            old_name='document_id',
            new_name='document',
        ),
        migrations.RenameField(
            model_name='documentaccess',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='documentaccess',
            name='access_granted_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
