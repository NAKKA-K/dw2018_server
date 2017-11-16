# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-16 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submission_form', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classification',
            old_name='id',
            new_name='my_id',
        ),
        migrations.RenameField(
            model_name='distribution',
            old_name='id',
            new_name='uuid',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='id',
            new_name='my_id',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='id',
            new_name='my_id',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='id',
            new_name='my_id',
        ),
        migrations.AlterField(
            model_name='submission',
            name='organization_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, to='submission_form.Organization'),
        ),
    ]
