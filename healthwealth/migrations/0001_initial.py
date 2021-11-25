# Generated by Django 3.1.8 on 2021-11-22 07:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import healthwealth.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(max_length=75)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email address')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Phone number')),
                ('birth_date', models.DateField(blank=True, default=None, null=True, verbose_name='Birth date')),
                ('address', models.TextField(default=None, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', healthwealth.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('1', 'Lab result'), ('2', 'Health recipe'), ('3', 'Health certificate')], max_length=1, null=True)),
                ('document_url', models.FileField(upload_to='')),
                ('title', models.CharField(max_length=100)),
                ('file_name', models.CharField(max_length=1000)),
                ('file_type', models.CharField(max_length=7)),
                ('description', models.TextField(default=None, null=True)),
                ('issuername', models.CharField(default=None, max_length=100, null=True)),
                ('issueddate', models.DateField(default=None, null=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Dokumen Kesehatan',
            },
        ),
    ]