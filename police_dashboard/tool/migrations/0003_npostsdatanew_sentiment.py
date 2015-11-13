# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0002_auto_20151112_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='npostsdatanew',
            name='sentiment',
            field=models.IntegerField(default=0, max_length=1),
            preserve_default=True,
        ),
    ]
