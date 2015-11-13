# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0003_npostsdatanew_sentiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npostsdatanew',
            name='sentiment',
            field=models.IntegerField(default=-1, max_length=1),
            preserve_default=True,
        ),
    ]
