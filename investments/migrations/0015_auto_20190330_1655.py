# Generated by Django 2.2b1 on 2019-03-30 15:55

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0014_investment_raw_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='efficency',
        ),
        migrations.AlterField(
            model_name='investment',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True),
        ),
        migrations.AlterField(
            model_name='investment',
            name='source',
            field=models.CharField(choices=[('caseinpiemonte', 'Case in Piemonte'), ('remicom', 'Remicom'), ('exploresardinia', 'Explore Sardinia'), ('sestrierecase', 'Sestriere case')], max_length=15),
        ),
    ]
