# Generated by Django 2.2 on 2019-07-20 13:49

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0029_auto_20190525_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='country',
            field=django_countries.fields.CountryField(default='IT', max_length=23, multiple=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='currency',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='description_it',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='meta_en',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='meta_it',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='raw_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='surface',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='tags',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='tags_en',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='tags_it',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='url',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
    ]
