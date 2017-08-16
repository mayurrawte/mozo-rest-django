# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mozorest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='transactionType',
            field=models.CharField(choices=[('refund', 'Refundable Transaction'), ('nonrefund', 'Non Refundable Transaction')], default='nonrefund', max_length=20),
        ),
    ]