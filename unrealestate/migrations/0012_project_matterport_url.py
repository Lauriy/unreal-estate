# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 12:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unrealestate', '0011_user_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='matterport_url',
            field=models.URLField(default='asd'),
            preserve_default=False,
        ),
    ]