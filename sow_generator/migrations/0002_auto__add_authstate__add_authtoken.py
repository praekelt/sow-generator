# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AuthState'
        db.create_table(u'sow_generator_authstate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'sow_generator', ['AuthState'])

        # Adding model 'AuthToken'
        db.create_table(u'sow_generator_authtoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=512)),
        ))
        db.send_create_signal(u'sow_generator', ['AuthToken'])


    def backwards(self, orm):
        # Deleting model 'AuthState'
        db.delete_table(u'sow_generator_authstate')

        # Deleting model 'AuthToken'
        db.delete_table(u'sow_generator_authtoken')


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
            'business': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'readme': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['sow_generator']