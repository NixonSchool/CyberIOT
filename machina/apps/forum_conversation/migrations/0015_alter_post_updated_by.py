# Generated by Django 5.0.8 on 2024-09-05 15:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_conversation', '0014_alter_post_id_alter_topic_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_posts', to=settings.AUTH_USER_MODEL, verbose_name='Lastly updated by'),
        ),
    ]
