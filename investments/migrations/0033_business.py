# Generated by Django 2.2 on 2019-08-07 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0032_auto_20190801_1753'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('investment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='investments.Investment')),
            ],
            options={
                'verbose_name': 'Business investment',
                'verbose_name_plural': 'Business investments',
            },
            bases=('investments.investment',),
        ),
    ]