# Generated by Django 3.1.7 on 2021-04-10 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_productvariants_filter_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariants',
            name='filter_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]