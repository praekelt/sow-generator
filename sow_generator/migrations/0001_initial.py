# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Repository'
        db.create_table(u'sow_generator_repository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('readme', self.gf('django.db.models.fields.TextField')(null=True)),
            ('business', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'sow_generator', ['Repository'])


    def backwards(self, orm):
        # Deleting model 'Repository'
        db.delete_table(u'sow_generator_repository')


    models = {
        u'sow_generator.repository': {
            'Meta': {'object_name': 'Repository'},
            'business': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'readme': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['sow_generator']