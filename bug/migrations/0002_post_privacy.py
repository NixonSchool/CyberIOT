# Generated by Django 5.0.8 on 2024-10-06 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='privacy',
            field=models.CharField(choices=[('private', 'Private'), ('public', 'Public')], default='public', max_length=10),
        ),
    ]
