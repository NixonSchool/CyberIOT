# Generated by Django 5.0.8 on 2024-09-13 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to='cover_photos/'),
        ),
    ]
