# pylint: disable=C0103,E1103

from datetime import datetime, timedelta
from os.path import join

from django.test import TestCase

from .models import Workshop, Application


class WorkshopsTestCase(TestCase):
    def setUp(self):
        self.w = {}
        now = datetime.now()

        self.w[0] = Workshop.objects.create(
            title='Test workshop', location='Monaco', instructor='James Bond',
            start_date=now + timedelta(hours=1), end_date=now + timedelta(hours=2))
        self.w[1] = Workshop.objects.create(
            title='Test workshop 2', location='Malta', instructor='Pinocchio',
            start_date=now + timedelta(days=1), end_date=now + timedelta(days=2))

        self.post_data = {
            'name': u'Janez Novak',
            'email': u'janez.novak@example.com',
            'institution_name': u'White house',
            str(self.w[0].pk): True,
        }

        self.url = '/delavnice/'

    def test_template_used(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('workshops', 'application.html'))

    def test_context(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['workshops']), 2)
        self.assertEqual(resp.context['workshops'][0], self.w[0])
        self.assertEqual(resp.context['workshops'][1], self.w[1])
        self.assertEqual(resp.context['msg'], '')
        self.assertEqual(resp.context['type'], 0)
        self.assertEqual(resp.context['msg'], '')
        self.assertEqual(resp.context['institution'], False)
        self.assertEqual(resp.context['name'], '')
        self.assertEqual(resp.context['email'], '')
        self.assertEqual(resp.context['institution_name'], '')
        self.assertEqual(resp.context['n_of_applicants'], '')
        self.assertEqual(resp.context['selected'][self.w[0].pk], False)
        self.assertEqual(resp.context['selected'][self.w[1].pk], False)

    def test_redirect_to_confirm(self):
        resp = self.client.post(self.url, data=self.post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('workshops', 'confirm.html'))

    def test_empty_request(self):
        resp = self.client.post(self.url, data={})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('workshops', 'application.html'))
        self.assertEqual(resp.context['type'], 46)
        self.assertNotEqual(resp.context['msg'], '')

    def test_single_application_count_as_one(self):
        self.post_data['n_of_applicants'] = 3
        resp = self.client.post(self.url, data=self.post_data)
        self.assertEqual(resp.status_code, 302)
        application = Application.objects.all()[0]
        self.assertEqual(application.n_of_applicants, 1)

    def test_dont_show_outdated_workshops(self):
        self.w[0].start_date = self.w[0].start_date - timedelta(days=10)
        self.w[0].end_date = self.w[0].end_date - timedelta(days=10)
        self.w[0].save()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['workshops']), 1)

    def test_model_count(self):
        del self.post_data[str(self.w[0].pk)]
        Application.objects.create(
            workshop=self.w[0], institution=False, n_of_applicants=1,
            **self.post_data)
        Application.objects.create(
            workshop=self.w[1], institution=False, n_of_applicants=1,
            **self.post_data)
        Application.objects.create(
            workshop=self.w[0], institution=True, n_of_applicants=4,
            **self.post_data)
        self.assertEqual(self.w[0].count(), 5)
        self.assertEqual(self.w[1].count(), 1)

    def test_n_of_applicants_not_returned_if_not_given(self):
        resp = self.client.post(self.url, data={})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['n_of_applicants'], '')
        resp = self.client.post(self.url, data={'institution': True})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['n_of_applicants'], '')

    def test_missing_name(self):
        data = self.post_data
        del data['name']
        resp = self.client.post(self.url, data=data)
        context = resp.context
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('workshops', 'application.html'))
        self.assertEqual(context['type'], 2)
        self.assertNotEqual(context['msg'], '')

        self.assertEqual(context['name'], '')
        self.assertEqual(context['email'], data['email'])
        self.assertEqual(context['institution_name'], data['institution_name'])
        self.assertEqual(context['selected'][self.w[0].pk], True)
        self.assertEqual(context['selected'][self.w[1].pk], False)

    def test_missing_email(self):
        data = self.post_data
        del data['email']
        resp = self.client.post(self.url, data=data)
        context = resp.context
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('workshops', 'application.html'))
        self.assertEqual(context['type'], 4)
        self.assertNotEqual(context['msg'], '')

        self.assertEqual(context['name'], data['name'])
        self.assertEqual(context['email'], '')
        self.assertEqual(context['institution_name'], data['institution_name'])
        self.assertEqual(context['selected'][self.w[0].pk], True)
        self.assertEqual(context['selected'][self.w[1].pk], False)

    def test_missing_institution_name(self):
        data = self.post_data
        del data['institution_name']
        resp = self.client.post(self.url, data=data)
        context = resp.context
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('workshops', 'application.html'))
        self.assertEqual(context['type'], 8)
        self.assertNotEqual(context['msg'], '')

        self.assertEqual(context['name'], data['name'])
        self.assertEqual(context['email'], data['email'])
        self.assertEqual(context['institution_name'], '')
        self.assertEqual(context['selected'][self.w[0].pk], True)
        self.assertEqual(context['selected'][self.w[1].pk], False)

    def test_n_of_applicants_required_for_institutions(self):
        data = self.post_data
        data['institution'] = True
        resp = self.client.post(self.url, data=data)
        context = resp.context
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('workshops', 'application.html'))
        self.assertEqual(context['type'], 16)
        self.assertNotEqual(context['msg'], '')

        self.assertEqual(context['name'], data['name'])
        self.assertEqual(context['email'], data['email'])
        self.assertEqual(context['institution_name'], data['institution_name'])
        self.assertEqual(context['selected'][self.w[0].pk], True)
        self.assertEqual(context['selected'][self.w[1].pk], False)

    def test_missing_workshop(self):
        data = self.post_data
        del data[str(self.w[0].pk)]
        resp = self.client.post(self.url, data=self.post_data)
        context = resp.context
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('workshops', 'application.html'))
        self.assertEqual(context['type'], 32)
        self.assertNotEqual(context['msg'], '')

        self.assertEqual(context['name'], data['name'])
        self.assertEqual(context['email'], data['email'])
        self.assertEqual(context['institution_name'], data['institution_name'])
        self.assertEqual(context['selected'][self.w[0].pk], False)
        self.assertEqual(context['selected'][self.w[1].pk], False)
