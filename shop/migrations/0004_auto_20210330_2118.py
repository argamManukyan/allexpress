# Generated by Django 3.1.7 on 2021-03-30 17:18

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210325_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Անուն')),
                ('icon', models.FileField(upload_to='brand_icons/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Բրենդ',
                'verbose_name_plural': 'Բրենդ',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Անուն')),
                ('code', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Գույն',
                'verbose_name_plural': 'Գույն',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Անուն')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Հղում')),
                ('manufactured', models.CharField(max_length=150, verbose_name='Արտադրող')),
                ('country', models.CharField(max_length=150, verbose_name='Արտադրող երկիր')),
                ('volume', models.CharField(blank=True, max_length=50, verbose_name='Ծավալ')),
                ('weight', models.CharField(blank=True, max_length=50, verbose_name='Քաշ')),
                ('power', models.CharField(blank=True, max_length=50, verbose_name='Հզորություն')),
                ('sort', models.CharField(blank=True, max_length=50, verbose_name='Տեսակ')),
                ('qty_in_coll', models.CharField(max_length=50, verbose_name='Քանակը հավաքածուում')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ապրանք',
                'verbose_name_plural': 'Ապրանք',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description',
            field=models.TextField(max_length=300, verbose_name='Մետա նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description_en',
            field=models.TextField(max_length=300, null=True, verbose_name='Մետա նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description_hy',
            field=models.TextField(max_length=300, null=True, verbose_name='Մետա նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description_ru',
            field=models.TextField(max_length=300, null=True, verbose_name='Մետա նկարագրություն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title',
            field=models.CharField(max_length=200, verbose_name='Մետա անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Մետա անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title_hy',
            field=models.CharField(max_length=200, null=True, verbose_name='Մետա անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Մետա անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_hy',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Անուն'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.category', verbose_name='Հայրական բաժին'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, unique=True, verbose_name='Հղում'),
        ),
        migrations.CreateModel(
            name='ProductVariants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50)),
                ('product_code', models.CharField(max_length=15)),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.color')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariantImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='product_images/')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.productvariants')),
            ],
        ),
    ]
