# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-24 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('opening', models.FloatField()),
                ('close', models.FloatField()),
                ('volume', models.IntegerField()),
            ],
        ),
    ]
