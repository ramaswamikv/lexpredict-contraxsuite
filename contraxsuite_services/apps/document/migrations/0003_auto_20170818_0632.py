# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 06:32
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('document', '0002_auto_20170731_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentproperty',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_documentproperty_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentproperty',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=datetime.datetime(2017, 8, 18, 6, 32, 9, 550047, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documentproperty',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_documentproperty_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentproperty',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AddField(
            model_name='textunitproperty',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_textunitproperty_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='textunitproperty',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=datetime.datetime(2017, 8, 18, 6, 32, 32, 949181, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textunitproperty',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_textunitproperty_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='textunitproperty',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]