# Generated by Django 5.0.8 on 2024-10-07 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketitem', '0005_remove_item_is_sold_item_available_from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='monthly_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('sold_out', 'Sold Out'), ('coming_soon', 'Coming Soon'), ('unavailable', 'Currently Unavailable'), ('subscription', 'Monthly Subscription')], default='available', max_length=20),
        ),
    ]
