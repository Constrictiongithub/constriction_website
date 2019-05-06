import uuid

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0007_auto_20190323_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Investment',
            name='identifier',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
