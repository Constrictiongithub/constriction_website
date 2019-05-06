# Generated by Django 2.2b1 on 2019-04-08 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0019_auto_20190402_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='country',
            field=models.CharField(choices=[('italy', 'Italia'), ('germany', 'Deutschland'), ('france', 'France'), ('switzerland', 'Schweizerische')], default='italy', max_length=15),
        ),
    ]
