# Generated by Django 3.1.7 on 2021-03-31 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_sliders'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariants',
            name='size_en',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='productvariants',
            name='size_hy',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='productvariants',
            name='size_ru',
            field=models.CharField(max_length=50, null=True),
        ),
    ]