# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-01 20:46
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

from apps.document import constants


class Migration(migrations.Migration):
    dependencies = [
        ('project', '0011_auto_20180324_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.ForeignKey(blank=True, default=constants.DOCUMENT_TYPE_PK_GENERIC_DOCUMENT, null=True,
                                    on_delete=django.db.models.deletion.CASCADE, to='document.DocumentType'),
        ),
    ]
