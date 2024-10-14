# Generated by Django 5.0.8 on 2024-09-26 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_permission', '0006_alter_forumpermission_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupforumpermission',
            name='has_perm',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Has permission'),
        ),
        migrations.AlterField(
            model_name='userforumpermission',
            name='has_perm',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Has permission'),
        ),
    ]
