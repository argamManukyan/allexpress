# Generated by Django 3.1.7 on 2021-03-25 16:41

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatepages', '0002_auto_20210325_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='content_en',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='content_hy',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='content_ru',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='content_en',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='content_hy',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='content_ru',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_description_en',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_description_hy',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_description_ru',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_title_en',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_title_hy',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_title_ru',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='short_description_en',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='short_description_hy',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='short_description_ru',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='title_en',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='title_hy',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='title_ru',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='ddeliveryandpayment',
            name='content_en',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='ddeliveryandpayment',
            name='content_hy',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='ddeliveryandpayment',
            name='content_ru',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_hy',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='answer_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='question_en',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='question_hy',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='faq',
            name='question_ru',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='howorder',
            name='content_en',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='howorder',
            name='content_hy',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='howorder',
            name='content_ru',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='returnproduct',
            name='content_en',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='returnproduct',
            name='content_hy',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name='returnproduct',
            name='content_ru',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
