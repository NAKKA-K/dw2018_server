# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-29 17:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('submission_form', '0002_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='published_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='作成日'),
        ),
        migrations.AlterField(
            model_name='classification',
            name='name',
            field=models.CharField(max_length=64, verbose_name='カテゴリ名'),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='classification_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submission_form.Classification', verbose_name='カテゴリ'),
        ),
        migrations.AlterField(
            model_name='distribution',
            name='published_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='作成日'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='published_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='classification_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submission_form.Classification', verbose_name='科目'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(help_text='xxxx-xx-xx の形式で入力してください', verbose_name='提出期限'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=64, verbose_name='提出ファイル名'),
        ),
        migrations.AlterField(
            model_name='task',
            name='text',
            field=models.TextField(verbose_name='説明'),
        ),
    ]