# Generated by Django 2.2.4 on 2019-12-23 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0172_auto_20191206_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfield',
            name='confidence',
            field=models.CharField(blank=True, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='documentfield',
            name='python_coded_field',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='documentfield',
            name='text_unit_type',
            field=models.CharField(choices=[('sentence', 'sentence'), ('paragraph', 'paragraph'), ('section', 'section')], default='sentence', max_length=10),
        ),
        migrations.AlterField(
            model_name='fieldannotation',
            name='extraction_hint',
            field=models.CharField(blank=True, choices=[('TAKE_FIRST', 'TAKE_FIRST'), ('TAKE_SECOND', 'TAKE_SECOND'), ('TAKE_LAST', 'TAKE_LAST'), ('TAKE_MIN', 'TAKE_MIN'), ('TAKE_MAX', 'TAKE_MAX')], default='TAKE_FIRST', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='historicalfieldannotation',
            name='extraction_hint',
            field=models.CharField(blank=True, choices=[('TAKE_FIRST', 'TAKE_FIRST'), ('TAKE_SECOND', 'TAKE_SECOND'), ('TAKE_LAST', 'TAKE_LAST'), ('TAKE_MIN', 'TAKE_MIN'), ('TAKE_MAX', 'TAKE_MAX')], default='TAKE_FIRST', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='textunit',
            name='language',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='textunit',
            name='text_hash',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='textunit',
            name='unit_type',
            field=models.CharField(max_length=128),
        ),
        migrations.AddIndex(
            model_name='documentfield',
            index=models.Index(fields=['text_unit_type'], name='document_do_text_un_74f361_idx'),
        ),
        migrations.AddIndex(
            model_name='documentfield',
            index=models.Index(fields=['confidence'], name='document_do_confide_63936a_idx'),
        ),
        migrations.AddIndex(
            model_name='documentfield',
            index=models.Index(fields=['python_coded_field'], name='document_do_python__89da0f_idx'),
        ),
        migrations.AddIndex(
            model_name='fieldannotation',
            index=models.Index(fields=['extraction_hint'], name='document_fi_extract_ca8e0c_idx'),
        ),
        migrations.AddIndex(
            model_name='textunit',
            index=models.Index(fields=['text_hash'], name='document_te_text_ha_11d6ee_idx'),
        ),
        migrations.AddIndex(
            model_name='textunit',
            index=models.Index(fields=['unit_type'], name='document_te_unit_ty_229aa3_idx'),
        ),
        migrations.AddIndex(
            model_name='textunit',
            index=models.Index(fields=['language'], name='document_te_languag_e69159_idx'),
        ),
    ]