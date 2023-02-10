# Generated by Django 4.1.6 on 2023-02-10 06:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_category_height_category_width_alter_category_photo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='height',
        ),
        migrations.RemoveField(
            model_name='category',
            name='width',
        ),
        migrations.AlterField(
            model_name='category',
            name='photo',
            field=models.ImageField(upload_to='photos/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='packing_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 10, 2, 29, 31, 879451)),
        ),
        migrations.AlterField(
            model_name='product',
            name='sell_before',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 17, 6, 29, 31, 879472)),
        ),
    ]
