# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table('training_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('is_a', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('interests', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('notify', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('training', ['Profile'])

        # Adding model 'Category'
        db.create_table('training_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('training', ['Category'])

        # Adding model 'Module'
        db.create_table('training_module', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('notes_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('training', ['Module'])

        # Adding M2M table for field categories on 'Module'
        m2m_table_name = db.shorten_name('training_module_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module', models.ForeignKey(orm['training.module'], null=False)),
            ('category', models.ForeignKey(orm['training.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module_id', 'category_id'])

        # Adding model 'Completion'
        db.create_table('training_completion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='completions', to=orm['auth.User'])),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(related_name='completions', to=orm['training.Module'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal('training', ['Completion'])

        # Adding model 'Training'
        db.create_table('training_training', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('training', ['Training'])

        # Adding model 'Feedback'
        db.create_table('training_feedback', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feedback', to=orm['auth.User'])),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(related_name='feedback', to=orm['training.Module'])),
            ('knowledge_before', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('knowledge_after', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('content_clarity', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('suggestions', self.gf('django.db.models.fields.TextField')()),
            ('positives', self.gf('django.db.models.fields.TextField')()),
            ('would_recommend', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
        ))
        db.send_create_signal('training', ['Feedback'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table('training_profile')

        # Deleting model 'Category'
        db.delete_table('training_category')

        # Deleting model 'Module'
        db.delete_table('training_module')

        # Removing M2M table for field categories on 'Module'
        db.delete_table(db.shorten_name('training_module_categories'))

        # Deleting model 'Completion'
        db.delete_table('training_completion')

        # Deleting model 'Training'
        db.delete_table('training_training')

        # Deleting model 'Feedback'
        db.delete_table('training_feedback')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'training.category': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'training.completion': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Completion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'completions'", 'to': "orm['training.Module']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'completions'", 'to': "orm['auth.User']"})
        },
        'training.feedback': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Feedback'},
            'content_clarity': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'knowledge_after': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'knowledge_before': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feedback'", 'to': "orm['training.Module']"}),
            'positives': ('django.db.models.fields.TextField', [], {}),
            'suggestions': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feedback'", 'to': "orm['auth.User']"}),
            'would_recommend': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'training.module': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Module'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'modules'", 'symmetrical': 'False', 'to': "orm['training.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'training.profile': {
            'Meta': {'ordering': "('user__username',)", 'object_name': 'Profile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_a': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'training.training': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Training'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['training']