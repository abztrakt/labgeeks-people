# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'WageHistory.wage_change_reason'
        db.alter_column(u'labgeeks_people_wagehistory', 'wage_change_reason_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['labgeeks_people.WageChangeReason']))

        # Changing field 'WageHistory.user'
        db.alter_column(u'labgeeks_people_wagehistory', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']))
        # Removing M2M table for field working_periods on 'UserProfile'
        db.delete_table(db.shorten_name(u'labgeeks_people_userprofile_working_periods'))


        # Changing field 'UserProfile.user'
        db.alter_column(u'labgeeks_people_userprofile', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, unique=True, to=orm['auth.User']))

        # Changing field 'PerformanceReview.user'
        db.alter_column(u'labgeeks_people_performancereview', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']))

        # Changing field 'PerformanceReview.reviewer'
        db.alter_column(u'labgeeks_people_performancereview', 'reviewer_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']))

    def backwards(self, orm):

        # Changing field 'WageHistory.wage_change_reason'
        db.alter_column(u'labgeeks_people_wagehistory', 'wage_change_reason_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labgeeks_people.WageChangeReason'], null=True))

        # Changing field 'WageHistory.user'
        db.alter_column(u'labgeeks_people_wagehistory', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))
        # Adding M2M table for field working_periods on 'UserProfile'
        m2m_table_name = db.shorten_name(u'labgeeks_people_userprofile_working_periods')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['labgeeks_people.userprofile'], null=False)),
            ('timeperiod', models.ForeignKey(orm['labgeeks_horae.timeperiod'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'timeperiod_id'])


        # Changing field 'UserProfile.user'
        db.alter_column(u'labgeeks_people_userprofile', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(unique=True, null=True, to=orm['auth.User']))

        # Changing field 'PerformanceReview.user'
        db.alter_column(u'labgeeks_people_performancereview', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'PerformanceReview.reviewer'
        db.alter_column(u'labgeeks_people_performancereview', 'reviewer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'labgeeks_people.employmentstatus': {
            'Meta': {'object_name': 'EmploymentStatus'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'labgeeks_people.paygrade': {
            'Meta': {'object_name': 'PayGrade'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'wage': ('django.db.models.fields.FloatField', [], {})
        },
        u'labgeeks_people.performancereview': {
            'Meta': {'object_name': 'PerformanceReview'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_final': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_used_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_review'", 'to': u"orm['auth.User']"})
        },
        u'labgeeks_people.title': {
            'Meta': {'object_name': 'Title'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'pay_grade': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labgeeks_people.PayGrade']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'workgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labgeeks_people.WorkGroup']"})
        },
        u'labgeeks_people.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'alt_phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'badge_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'call_me_by': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'grad_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'staff_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labgeeks_people.EmploymentStatus']", 'null': 'True', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'supervisor'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labgeeks_people.Title']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uwnetid'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'wage': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['labgeeks_people.WageHistory']", 'null': 'True', 'blank': 'True'})
        },
        u'labgeeks_people.uwltreview': {
            'Meta': {'object_name': 'UWLTReview', '_ormbases': [u'labgeeks_people.PerformanceReview']},
            'attitude': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'attitude_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'communication': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'communication_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'customer_service': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'customer_service_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dependability': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dependability_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'initiative': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'initiative_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'integrity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'integrity_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'missed_shifts': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'missed_shifts_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'performancereview_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['labgeeks_people.PerformanceReview']", 'unique': 'True', 'primary_key': 'True'}),
            'policies': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'policies_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'procedures': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'procedures_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'productivity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'productivity_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'responsibility': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'responsibility_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tardies': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tardies_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'teamwork': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'teamwork_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'technical_knowledge': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'technical_knowledge_comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'weights': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labgeeks_people.UWLTReviewWeights']", 'null': 'True', 'blank': 'True'})
        },
        u'labgeeks_people.uwltreviewweights': {
            'Meta': {'object_name': 'UWLTReviewWeights'},
            'attitude_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'communication_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'customer_service_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'dependability_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'effective_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiative_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'integrity_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'policies_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'procedures_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'productivity_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'responsibility_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'teamwork_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'technical_knowledge_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'})
        },
        u'labgeeks_people.wagechangereason': {
            'Meta': {'object_name': 'WageChangeReason'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'labgeeks_people.wagehistory': {
            'Meta': {'object_name': 'WageHistory'},
            'effective_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'wage': ('django.db.models.fields.FloatField', [], {}),
            'wage_change_reason': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['labgeeks_people.WageChangeReason']"})
        },
        u'labgeeks_people.workgroup': {
            'Meta': {'object_name': 'WorkGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['labgeeks_people']