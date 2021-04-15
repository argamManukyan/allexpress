# Generated by Django 3.1.7 on 2021-04-15 05:24

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_auto_20210410_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariants',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sliders',
            name='context',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='sliders',
            name='context_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='sliders',
            name='context_hy',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='sliders',
            name='context_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='specialoffer',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='specialoffer',
            name='description_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='specialoffer',
            name='description_hy',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='specialoffer',
            name='description_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Նկարագրություն'),
        ),
    ]