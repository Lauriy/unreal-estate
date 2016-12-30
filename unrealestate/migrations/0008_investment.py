# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 15:47
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('unrealestate', '0007_auto_20161228_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('value_currency', djmoney.models.fields.CurrencyField(choices=[('SGD', 'Singapore Dollar')], default='SGD', editable=False, max_length=3)),
                ('value', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='SGD', max_digits=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='unrealestate.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]