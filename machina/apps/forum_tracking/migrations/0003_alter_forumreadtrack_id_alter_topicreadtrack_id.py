# Generated by Django 5.0 on 2024-08-20 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_tracking', '0002_auto_20160607_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumreadtrack',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='topicreadtrack',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]