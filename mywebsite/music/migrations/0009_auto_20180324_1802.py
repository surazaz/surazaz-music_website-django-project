# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-24 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_auto_20171023_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_logo',
            field=models.FileField(max_length=1000, upload_to=''),
        ),
    ]
