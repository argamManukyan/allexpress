# Generated by Django 3.1.7 on 2021-04-01 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20210331_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariants',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productvariants',
            name='sale',
            field=models.IntegerField(default=0),
        ),
    ]