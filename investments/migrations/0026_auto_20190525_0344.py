# Generated by Django 2.2 on 2019-05-25 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0025_auto_20190524_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentimage',
            name='image',
            field=models.ImageField(upload_to="uploads/investments"),
        ),
    ]
