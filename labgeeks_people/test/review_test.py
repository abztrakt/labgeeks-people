"""
tests review creation and viewing (validity and permissions)
"""

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from forms_builder.forms.models import *
from labgeeks_people.models import *
import datetime


class ReviewTestCase(TestCase):

    def setUp(self):
        """
        Preps the test db for permissions testing
        """
        self.dawg = User.objects.create_user('Dawg', 'dawg@test.com', 'pass')
        self.dawg.save()
        self.manager = User.objects.create_user('Manager', 'dawgm@test.com', 'pass')
        ct = ContentType.objects.get_for_model(UWLTReview)
        addReview = Permission.objects.get(content_type=ct, codename='add_uwltreview')
        finalize = Permission.objects.get(content_type=ct, codename='finalize_review')
        self.manager.user_permissions.add(addReview)
        self.manager.save()
        self.bigboss = User.objects.create_user('BigBoss', 'dawgb@test.com', 'pass')
        self.bigboss.user_permissions.add(addReview)
        self.bigboss.user_permissions.add(finalize)
        self.bigboss.save()
        d = datetime.date.today()
        self.reviewform = ReviewForm.objects.create()
        self.dawgreview = ReviewFormEntry.objects.create(reviewing=self.dawg, form=self.reviewform, official=True, reviewer=self.bigboss, complete=True)
        self.managerreview = ReviewFormEntry.objects.create(reviewing=self.manager, form=self.reviewform, official=True, reviewer=self.bigboss, complete=True)
        self.dawgprofile = UserProfile.objects.create(user=self.dawg)
        self.managerprofile = UserProfile.objects.create(user=self.manager)
        self.bigbossprofile = UserProfile.objects.create(user=self.bigboss)

    def testStaffPermissions(self):
        """
        Tests permissions for basic staff member
        """
        c = Client()
        c.login(username="Dawg", password='pass')
        resp1 = c.get('/people/Dawg/view_reviews/')
        self.assertEqual(resp1.status_code, 200)  # access to his own json review I guess
        resp2 = c.get('/people/Dawg/review/')
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, "Reviews for Dawg")
        resp3 = c.post('/people/Dawg/review/', {'reviewing': 'Dawg', 'reviewer': 'Dawg', 'complete': True, 'awesomeness': 5, 'comments': 'Dawg is a cool dawg'}, follow=True)
        self.assertEqual(resp3.status_code, 200)
        c.logout()

    def testManagerPermissions(self):
        """
        Tests permissions for someone who can add reviews but is
        not a superuser/final reviewer
        """
        c = Client()
        c.login(username="Manager", password='pass')
        resp1 = c.get('/people/Manager/view_reviews/')
        self.assertEqual(resp1.status_code, 200)
        self.assertContains(resp1, 'Reviews for Manager')
        resp2 = c.get('/people/Dawg/view_reviews/')
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, "Official Reviews for Dawg")
        resp = c.get('/people/Dawg/review/')
        self.assertEqual(resp.status_code, 200)
        resp3 = c.get('/people/BigBoss/view_reviews/')
        self.assertEqual(resp3.status_code, 200)
        c.logout()

    def testBigBossPermissions(self):
        """
        Tests permissions for superuser/final reviewer
        """
        c = Client()
        c.login(username="BigBoss", password='pass')
        resp1 = c.get('/people/Manager/view_reviews/')
        self.assertEqual(resp1.status_code, 200)
        resp = c.get('/people/Manager/review/')
        self.assertEqual(resp.status_code, 200)
        resp2 = c.get('/people/BigBoss/review/')
        self.assertEqual(resp2.status_code, 200)
        c.logout()

    def testReviewForm(self):
        pass

    def testReviewFormEtnry(self):
        pass

    def 
