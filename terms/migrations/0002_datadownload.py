# Generated by Django 5.0.8 on 2024-09-10 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataDownload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]
