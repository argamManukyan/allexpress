# Generated by Django 3.1.7 on 2021-04-02 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_auto_20210402_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='meta_description',
            field=models.TextField(blank=True, max_length=300, verbose_name='Մետա նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description_en',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Մետա նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description_hy',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Մետա նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description_ru',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Մետա նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title',
            field=models.CharField(blank=True, max_length=200, verbose_name='Մետա անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Մետա անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title_hy',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Մետա անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title_ru',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Մետա անուն'),
        ),
    ]
