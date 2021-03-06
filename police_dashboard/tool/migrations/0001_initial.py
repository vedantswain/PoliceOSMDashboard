# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NPostsdatanew',
            fields=[
                ('localid', models.IntegerField(serialize=False, primary_key=True)),
                ('id', models.CharField(unique=True, max_length=200, blank=True)),
                ('message', models.TextField(blank=True)),
                ('story', models.CharField(max_length=100, blank=True)),
                ('picture', models.CharField(max_length=200, blank=True)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('link', models.CharField(max_length=200, blank=True)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('caption', models.CharField(max_length=500, blank=True)),
                ('application', models.CharField(max_length=300, blank=True)),
                ('fromid', models.CharField(max_length=100, blank=True)),
                ('created_time', models.CharField(max_length=100, blank=True)),
                ('updated_time', models.CharField(max_length=100, blank=True)),
                ('totallikescount', models.CharField(max_length=200, blank=True)),
                ('totalcommentscount', models.CharField(max_length=200, blank=True)),
                ('pageid', models.CharField(max_length=1000, blank=True)),
                ('id_public', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'db_table': 'N_Postsdatanew',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
