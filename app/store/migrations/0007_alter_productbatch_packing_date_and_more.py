# Generated by Django 4.1.6 on 2023-02-28 10:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_productbatch_packing_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbatch',
            name='packing_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 28, 6, 49, 32, 710699)),
        ),
        migrations.AlterField(
            model_name='productbatch',
            name='sell_before',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 7, 10, 49, 32, 710718)),
        ),
    ]
