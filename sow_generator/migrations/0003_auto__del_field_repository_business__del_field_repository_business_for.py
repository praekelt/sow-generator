# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Repository.business'
        db.delete_column(u'sow_generator_repository', 'business')

        # Deleting field 'Repository.business_format'
        db.delete_column(u'sow_generator_repository', 'business_format')

        # Adding field 'Repository.sow'
        db.add_column(u'sow_generator_repository', 'sow',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Repository.sow_format'
        db.add_column(u'sow_generator_repository', 'sow_format',
                      self.gf('django.db.models.fields.CharField')(max_length=8, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Repository.business'
        db.add_column(u'sow_generator_repository', 'business',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Repository.business_format'
        db.add_column(u'sow_generator_repository', 'business_format',
                      self.gf('django.db.models.fields.CharField')(max_length=8, null=True),
                      keep_default=False)

        # Deleting field 'Repository.sow'
        db.delete_column(u'sow_generator_repository', 'sow')

        # Deleting field 'Repository.sow_format'
        db.delete_column(u'sow_generator_repository', 'sow_format')


    models = {
        u'sow_generator.authstate': {
            'Meta': {'object_name': 'AuthState'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'sow_generator.authtoken': {
            'Meta': {'object_name': 'AuthToken'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'sow_generator.repository': {
            'Meta': {'object_name': 'Repository'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'readme': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'readme_format': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'sow': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'sow_format': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'})
        }
    }

    complete_apps = ['sow_generator']