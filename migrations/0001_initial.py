# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        from django.db import connections, DEFAULT_DB_ALIAS
        connection = connections[DEFAULT_DB_ALIAS]
        if 'mysql' in connection.settings_dict['ENGINE']:
            cursor = connection.cursor()
            cursor.execute('SET foreign_key_checks = 0')

        # Adding model 'EmploymentStatus'
        db.create_table('labgeeks_people_employmentstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('labgeeks_people', ['EmploymentStatus'])

        # Adding model 'WorkGroup'
        db.create_table('labgeeks_people_workgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('labgeeks_people', ['WorkGroup'])

        # Adding model 'PayGrade'
        db.create_table('labgeeks_people_paygrade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('wage', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('labgeeks_people', ['PayGrade'])

        # Adding model 'Title'
        db.create_table('labgeeks_people_title', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('workgroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labgeeks_people.WorkGroup'])),
            ('pay_grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labgeeks_people.PayGrade'])),
        ))
        db.send_create_signal('labgeeks_people', ['Title'])

        # Adding model 'WageChangeReason'
        db.create_table('labgeeks_people_wagechangereason', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('labgeeks_people', ['WageChangeReason'])

        # Adding model 'WageHistory'
        db.create_table('labgeeks_people_wagehistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('effective_date', self.gf('django.db.models.fields.DateField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('wage', self.gf('django.db.models.fields.FloatField')()),
            ('wage_change_reason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labgeeks_people.WageChangeReason'], null=True, blank=True)),
        ))
        db.send_create_signal('labgeeks_people', ['WageHistory'])

        # Adding model 'UWLTReviewWeights'
        db.create_table('labgeeks_people_uwltreviewweights', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('effective_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today, blank=True)),
            ('teamwork_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('customer_service_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('dependability_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('integrity_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('communication_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('initiative_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('attitude_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('productivity_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('technical_knowledge_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('responsibility_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('policies_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('procedures_multiplier', self.gf('django.db.models.fields.FloatField')(default=1)),
        ))
        db.send_create_signal('labgeeks_people', ['UWLTReviewWeights'])

        # Adding model 'PerformanceReview'
        db.create_table('labgeeks_people_performancereview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_review', null=True, to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('is_used_up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_final', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('labgeeks_people', ['PerformanceReview'])

        # Adding model 'UWLTReview'
        db.create_table('labgeeks_people_uwltreview', (
            ('performancereview_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['labgeeks_people.PerformanceReview'], unique=True, primary_key=True)),
            ('teamwork', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('teamwork_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('customer_service', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('customer_service_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dependability', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dependability_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('integrity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('integrity_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('communication', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('communication_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('initiative', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('initiative_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attitude', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('attitude_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('productivity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('productivity_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('technical_knowledge', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('technical_knowledge_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('responsibility', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('responsibility_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('policies', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('policies_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('procedures', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('procedures_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('missed_shifts', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('missed_shifts_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tardies', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tardies_comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('weights', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labgeeks_people.UWLTReviewWeights'], null=True, blank=True)),
        ))
        db.send_create_signal('labgeeks_people', ['UWLTReview'])

        # Adding model 'UserProfile'
        db.create_table('labgeeks_people_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='uwnetid', unique=True, null=True, to=orm['auth.User'])),
            ('staff_photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('badge_photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('call_me_by', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labgeeks_people.EmploymentStatus'], null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('grad_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('supervisor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='supervisor', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labgeeks_people.Title'], null=True, blank=True)),
            ('office', self.gf('django.db.models.fields.CharField')(default='', max_length=256, null=True, blank=True)),
            ('about_me', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('alt_phone', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
        ))
        db.send_create_signal('labgeeks_people', ['UserProfile'])

        # Adding M2M table for field working_periods on 'UserProfile'
        db.create_table('labgeeks_people_userprofile_working_periods', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['labgeeks_people.userprofile'], null=False)),
            ('timeperiod', models.ForeignKey(orm['labgeeks_horae.timeperiod'], null=False))
        ))
        db.create_unique('labgeeks_people_userprofile_working_periods', ['userprofile_id', 'timeperiod_id'])

        # Adding M2M table for field wage on 'UserProfile'
        db.create_table('labgeeks_people_userprofile_wage', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['labgeeks_people.userprofile'], null=False)),
            ('wagehistory', models.ForeignKey(orm['labgeeks_people.wagehistory'], null=False))
        ))
        db.create_unique('labgeeks_people_userprofile_wage', ['userprofile_id', 'wagehistory_id'])

        if 'mysql' in connection.settings_dict['ENGINE']:
            cursor = connection.cursor()
            cursor.execute('SET foreign_key_checks = 1')
            connection.close()


    def backwards(self, orm):
        
        # Deleting model 'EmploymentStatus'
        db.delete_table('labgeeks_people_employmentstatus')

        # Deleting model 'WorkGroup'
        db.delete_table('labgeeks_people_workgroup')

        # Deleting model 'PayGrade'
        db.delete_table('labgeeks_people_paygrade')

        # Deleting model 'Title'
        db.delete_table('labgeeks_people_title')

        # Deleting model 'WageChangeReason'
        db.delete_table('labgeeks_people_wagechangereason')

        # Deleting model 'WageHistory'
        db.delete_table('labgeeks_people_wagehistory')

        # Deleting model 'UWLTReviewWeights'
        db.delete_table('labgeeks_people_uwltreviewweights')

        # Deleting model 'PerformanceReview'
        db.delete_table('labgeeks_people_performancereview')

        # Deleting model 'UWLTReview'
        db.delete_table('labgeeks_people_uwltreview')

        # Deleting model 'UserProfile'
        db.delete_table('labgeeks_people_userprofile')

        # Removing M2M table for field working_periods on 'UserProfile'
        db.delete_table('labgeeks_people_userprofile_working_periods')

        # Removing M2M table for field wage on 'UserProfile'
        db.delete_table('labgeeks_people_userprofile_wage')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 18, 22, 19, 4, 78208)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 18, 22, 19, 4, 78144)'}),
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
        'labgeeks_horae.timeperiod': {
            'Meta': {'object_name': 'TimePeriod'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 11, 18)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 11, 18)'})
        },
        'labgeeks_people.employmentstatus': {
            'Meta': {'object_name': 'EmploymentStatus'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'labgeeks_people.paygrade': {
            'Meta': {'object_name': 'PayGrade'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'wage': ('django.db.models.fields.FloatField', [], {})
        },
        'labgeeks_people.performancereview': {
            'Meta': {'object_name': 'PerformanceReview'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_final': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_used_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_review'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'labgeeks_people.title': {
            'Meta': {'object_name': 'Title'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'pay_grade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labgeeks_people.PayGrade']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'workgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labgeeks_people.WorkGroup']"})
        },
        'labgeeks_people.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'alt_phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'badge_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'call_me_by': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'grad_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'staff_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labgeeks_people.EmploymentStatus']", 'null': 'True', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'supervisor'", 'null': 'True', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labgeeks_people.Title']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'uwnetid'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'wage': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['labgeeks_people.WageHistory']", 'null': 'True', 'blank': 'True'}),
            'working_periods': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['labgeeks_horae.TimePeriod']", 'null': 'True', 'blank': 'True'})
        },
        'labgeeks_people.uwltreview': {
            'Meta': {'object_name': 'UWLTReview', '_ormbases': ['labgeeks_people.PerformanceReview']},
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
            'performancereview_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['labgeeks_people.PerformanceReview']", 'unique': 'True', 'primary_key': 'True'}),
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
            'weights': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labgeeks_people.UWLTReviewWeights']", 'null': 'True', 'blank': 'True'})
        },
        'labgeeks_people.uwltreviewweights': {
            'Meta': {'object_name': 'UWLTReviewWeights'},
            'attitude_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'communication_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'customer_service_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'dependability_multiplier': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'effective_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        'labgeeks_people.wagechangereason': {
            'Meta': {'object_name': 'WageChangeReason'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'labgeeks_people.wagehistory': {
            'Meta': {'object_name': 'WageHistory'},
            'effective_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'wage': ('django.db.models.fields.FloatField', [], {}),
            'wage_change_reason': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labgeeks_people.WageChangeReason']", 'null': 'True', 'blank': 'True'})
        },
        'labgeeks_people.workgroup': {
            'Meta': {'object_name': 'WorkGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['labgeeks_people']
