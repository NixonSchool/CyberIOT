# Generated by Django 5.0.8 on 2024-09-20 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_userprofile_address_userprofile_bio_userprofile_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]