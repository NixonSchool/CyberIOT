# Generated by Django 5.0.8 on 2024-10-06 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_user_password_reset_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_read_posts',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]