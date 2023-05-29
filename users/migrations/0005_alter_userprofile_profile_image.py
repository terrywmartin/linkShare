# Generated by Django 4.2.1 on 2023-05-29 16:04

import core.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='profiles/user-default.png', storage=core.storage_backends.PublicMediaStorage(), upload_to='profiles/'),
        ),
    ]