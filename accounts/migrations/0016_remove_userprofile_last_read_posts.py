# Generated by Django 5.0.8 on 2024-10-06 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_userprofile_last_read_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_read_posts',
        ),
    ]