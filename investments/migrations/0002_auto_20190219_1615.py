# Generated by Django 2.2b1 on 2019-02-19 15:15

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0001_initial_squashed_0008_auto_20190219_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title'),
        ),
    ]
