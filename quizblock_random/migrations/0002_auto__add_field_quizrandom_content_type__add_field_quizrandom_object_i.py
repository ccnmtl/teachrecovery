# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'QuizRandom.content_type'
        db.add_column(u'quizblock_random_quizrandom', 'content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'QuizRandom.object_id'
        db.add_column(u'quizblock_random_quizrandom', 'object_id',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'QuizRandom.content_type'
        db.delete_column(u'quizblock_random_quizrandom', 'content_type_id')

        # Deleting field 'QuizRandom.object_id'
        db.delete_column(u'quizblock_random_quizrandom', 'object_id')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'quizblock.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'allow_redo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rhetorical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_submit_state': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'quizblock_random.quizrandom': {
            'Meta': {'object_name': 'QuizRandom', '_ormbases': [u'quizblock.Quiz']},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'quiz_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'quiz_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['quizblock.Quiz']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['quizblock_random']