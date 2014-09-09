# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuizRandom'
        db.create_table(u'quizblock_random_quizrandom', (
            (u'quiz_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['quizblock.Quiz'], unique=True, primary_key=True)),
            ('quiz_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'quizblock_random', ['QuizRandom'])


    def backwards(self, orm):
        # Deleting model 'QuizRandom'
        db.delete_table(u'quizblock_random_quizrandom')


    models = {
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
            'quiz_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'quiz_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['quizblock.Quiz']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['quizblock_random']