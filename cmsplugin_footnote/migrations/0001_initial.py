# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20140926_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footnote',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('body', models.TextField(verbose_name='body')),
                ('symbol', models.CharField(help_text='Overrides the automatic numbering.', max_length=10, verbose_name='symbol', blank=True)),
            ],
            options={
                'db_table': 'cmsplugin_footnote',
                'verbose_name': 'Footnote',
                'verbose_name_plural': 'Footnotes',
            },
            bases=('cms.cmsplugin',),
        ),
    ]
