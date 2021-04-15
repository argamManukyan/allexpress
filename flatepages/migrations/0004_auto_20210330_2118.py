# Generated by Django 3.1.7 on 2021-03-30 17:18

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatepages', '0003_auto_20210325_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyAndPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField()),
                ('content_en', ckeditor.fields.RichTextField(null=True)),
                ('content_ru', ckeditor.fields.RichTextField(null=True)),
                ('content_hy', ckeditor.fields.RichTextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Պայմաններ և Դրույթներ',
                'verbose_name_plural': 'Պայմաններ և Դրույթներ',
            },
        ),
        migrations.CreateModel(
            name='TermsAndConditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField()),
                ('content_en', ckeditor.fields.RichTextField(null=True)),
                ('content_ru', ckeditor.fields.RichTextField(null=True)),
                ('content_hy', ckeditor.fields.RichTextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Պայմաններ և Դրույթներ',
                'verbose_name_plural': 'Պայմաններ և Դրույթներ',
            },
        ),
        migrations.RenameModel(
            old_name='DdeliveryAndPayment',
            new_name='DeliveryAndPayment',
        ),
    ]