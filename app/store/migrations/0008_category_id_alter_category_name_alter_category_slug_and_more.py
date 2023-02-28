# Generated by Django 4.1.6 on 2023-02-28 16:12

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_productbatch_packing_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default='Category1', on_delete=django.db.models.deletion.PROTECT, to='store.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_size',
            field=models.PositiveSmallIntegerField(default=10, validators=[django.core.validators.MaxValueValidator(limit_value=99)], verbose_name='discount'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(auto_created=True, default=True, verbose_name='available'),
        ),
        migrations.AlterField(
            model_name='product',
            name='measure',
            field=models.CharField(choices=[(None, 'Measure not chosen'), ('kg', 'Kg'), ('g', 'g'), ('l', 'L'), ('ml', 'mL')], max_length=5),
        ),
        migrations.AlterField(
            model_name='product',
            name='producer',
            field=models.ForeignKey(default='Producer1', on_delete=django.db.models.deletion.PROTECT, to='store.producer'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
        migrations.AlterField(
            model_name='productbatch',
            name='packing_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 28, 12, 11, 57, 148941)),
        ),
        migrations.AlterField(
            model_name='productbatch',
            name='sell_before',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 7, 16, 11, 57, 148960)),
        ),
    ]
