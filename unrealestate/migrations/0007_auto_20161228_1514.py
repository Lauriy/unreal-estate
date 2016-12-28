# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 15:14
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('unrealestate', '0006_auto_20161228_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Deposit'), (1, 'Withdrawal')])),
                ('amount_currency', djmoney.models.fields.CurrencyField(choices=[('SGD', 'Singapore Dollar')], default='SGD', editable=False, max_length=3)),
                ('amount', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0.0'), default_currency='SGD', max_digits=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='goal_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('SGD', 'Singapore Dollar')], default='SGD', editable=False, max_length=3),
        ),
    ]
