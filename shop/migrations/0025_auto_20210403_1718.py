# Generated by Django 3.1.7 on 2021-04-03 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_product_is_popular'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_popular',
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_description',
            field=models.TextField(blank=True, verbose_name='Մետա նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='product',
            name='meta_title',
            field=models.CharField(blank=True, max_length=200, verbose_name='Մետա անուն'),
        ),
    ]