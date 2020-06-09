# Generated by Django 2.2.10 on 2020-03-21 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extract', '0045_documenttermusage'),
    ]

    operations = [
        migrations.RunSQL(
            sql=r'''CREATE INDEX "extract_definitionusage_definition_upper_idx" 
            ON "extract_definitionusage" (UPPER("definition"));''',
            reverse_sql=r'DROP INDEX "extract_definitionusage_definition_upper_idx";'
        ),
    ]