# Generated by Django 3.1.7 on 2021-04-14 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_auto_20210410_1214'),
        ('wish', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='WishItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.productvariants')),
            ],
        ),
        migrations.DeleteModel(
            name='WishList',
        ),
        migrations.AddField(
            model_name='wish',
            name='items',
            field=models.ManyToManyField(to='wish.WishItem'),
        ),
    ]
