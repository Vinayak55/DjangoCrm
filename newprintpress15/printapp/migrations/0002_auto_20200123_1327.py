# Generated by Django 3.0.2 on 2020-01-23 07:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balance',
            name='orderid',
        ),
        migrations.RemoveField(
            model_name='balance',
            name='paymentid',
        ),
        migrations.AlterField(
            model_name='balance',
            name='Date',
            field=models.DateField(default=datetime.datetime(2020, 1, 23, 13, 27, 6, 975133)),
        ),
        migrations.AlterField(
            model_name='order',
            name='Date',
            field=models.DateField(default=datetime.datetime(2020, 1, 23, 13, 27, 6, 975133)),
        ),
        migrations.AlterField(
            model_name='payment',
            name='Date',
            field=models.DateField(default=datetime.datetime(2020, 1, 23, 13, 27, 6, 975133)),
        ),
    ]
