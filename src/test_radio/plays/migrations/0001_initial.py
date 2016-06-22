# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0001_initial'),
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_play', models.DateTimeField()),
                ('end_play', models.DateTimeField()),
                ('song', models.ForeignKey(related_name='song', to='songs.Song')),
                ('station', models.ForeignKey(related_name='station', to='station.Station')),
            ],
        ),
    ]
