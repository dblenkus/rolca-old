# -*- coding: utf-8 -*-
# pylint: disable=C0103,E1103
from __future__ import absolute_import, division, print_function, unicode_literals

from os.path import join

from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse

from .forms import UserProfileCreationForm  # , UserProfileChangeForm
from .models import Institution, Mentor, UserProfile


class LoginTestCase(TestCase):
    def setUp(self):
        mentor = Mentor.objects.create(name="Franc Horvat")
        self.user = UserProfile.objects.create_user(
            first_name="Janez", last_name="Novak", mentor=mentor,
            email="janez.novak@example.com", address="Zgornji Kašelj 42",
            post="1234 Zgornji Kašelj", school="OS Zgornji Kašelj")
        self.user.set_password('test_pwd')
        self.user.save()

        self.post_data = {'email': self.user.email, 'password': 'test_pwd'}

    def test_login_redirect_from_index(self):
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'login.html'))

    def test_login_logout(self):
        self.client.post(reverse('login'), self.post_data)
        self.assertEqual(self.client.session['_auth_user_id'], unicode(self.user.pk))

        self.client.get(reverse('logout'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_deny_without_email(self):
        del self.post_data['email']
        resp = self.client.post(reverse('login'), self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'login.html'))
        self.assertIn('email', resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')

        self.assertEqual(resp.context['email'], '')
        self.assertEqual(resp.context['password'], self.post_data['password'])

    def test_deny_without_password(self):
        del self.post_data['password']
        resp = self.client.post(reverse('login'), self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'login.html'))
        self.assertIn('password', resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')

        self.assertEqual(resp.context['email'], self.post_data['email'])
        self.assertEqual(resp.context['password'], '')

    def test_deny_with_wrong_password(self):
        self.post_data['password'] = 'wrong_pwd'
        resp = self.client.post(reverse('login'), self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'login.html'))
        self.assertIn('password', resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')

        self.assertEqual(resp.context['email'], self.post_data['email'])
        self.assertEqual(resp.context['password'], self.post_data['password'])

    def test_password_recovery(self):
        resp = self.client.get(reverse('password_reset'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'password_reset_form.html'))

        resp = self.client.post(
            reverse('password_reset'), {'email': self.user.email}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'password_reset_done.html'))

        self.assertEqual(len(mail.outbox), 1)

        message = mail.outbox[0]
        url = message.body.split('http://example.com')[1].split('\n', 1)[0]
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'password_reset_confirm.html'))

        resp = self.client.post(
            url, {'new_password1': 'new_pwd', 'new_password2': 'new_pwd'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'password_reset_complete.html'))

        u = UserProfile.objects.all()[0]  # plyint: disable=no-member
        self.assertTrue(u.check_password('new_pwd'))


class SignupTestCase(TestCase):
    def setUp(self):
        Institution.objects.create(name=u'OS Zgornji Kašelj')

        self.post_data = {
            u'first_name': u'Janez',
            u'last_name': u'Novak',
            u'email': u'janez.novak@example.com',
            u'address': u'Zgornji Kašelj 42',
            u'post': u'1234 Zgornji Kašelj',
            u'school': u'OS Zgornji Kašelj',
            u'mentor': u'Franc Horvat',
        }

        self.url = reverse('signup')

    def test_template_used(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup.html'))

    def test_successful_signup(self):
        resp = self.client.post(self.url, self.post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup_confirm.html'))
        self.assertEqual(len(mail.outbox), 1)

        users = UserProfile.objects.all()  # plyint: disable=no-member
        self.assertEqual(len(users), 1)

    def test_empty_post_request(self):
        resp = self.client.post(self.url, {})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup.html'))
        self.assertEqual(['first_name', 'last_name', 'email', 'address', 'post',
                          'school'], resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')
        self.assertEqual(len(mail.outbox), 0)

        self.assertEqual(resp.context['first_name'], '')
        self.assertEqual(resp.context['last_name'], '')
        self.assertEqual(resp.context['email'], '')
        self.assertEqual(resp.context['address'], '')
        self.assertEqual(resp.context['post'], '')
        self.assertEqual(resp.context['school'], '')
        self.assertEqual(resp.context['mentor'], '')

    def test_deny_without_first_name(self):
        del self.post_data['first_name']
        resp = self.client.post(self.url, self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup.html'))
        self.assertEqual(['first_name'], resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')
        self.assertEqual(len(mail.outbox), 0)

        self.assertEqual(resp.context['first_name'], '')
        self.assertEqual(resp.context['last_name'], self.post_data['last_name'])
        self.assertEqual(resp.context['email'], self.post_data['email'])
        self.assertEqual(resp.context['address'], self.post_data['address'])
        self.assertEqual(resp.context['post'], self.post_data['post'])
        self.assertEqual(resp.context['school'], self.post_data['school'])
        self.assertEqual(resp.context['mentor'], self.post_data['mentor'])

    def test_deny_without_last_name(self):
        del self.post_data['last_name']
        resp = self.client.post(self.url, self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup.html'))
        self.assertEqual(['last_name'], resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')
        self.assertEqual(len(mail.outbox), 0)

        self.assertEqual(resp.context['first_name'], self.post_data['first_name'])
        self.assertEqual(resp.context['last_name'], '')
        self.assertEqual(resp.context['email'], self.post_data['email'])
        self.assertEqual(resp.context['address'], self.post_data['address'])
        self.assertEqual(resp.context['post'], self.post_data['post'])
        self.assertEqual(resp.context['school'], self.post_data['school'])
        self.assertEqual(resp.context['mentor'], self.post_data['mentor'])

    def test_deny_without_email(self):
        del self.post_data['email']
        resp = self.client.post(self.url, self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup.html'))
        self.assertEqual(['email'], resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')
        self.assertEqual(len(mail.outbox), 0)

        self.assertEqual(resp.context['first_name'], self.post_data['first_name'])
        self.assertEqual(resp.context['last_name'], self.post_data['last_name'])
        self.assertEqual(resp.context['email'], '')
        self.assertEqual(resp.context['address'], self.post_data['address'])
        self.assertEqual(resp.context['post'], self.post_data['post'])
        self.assertEqual(resp.context['school'], self.post_data['school'])
        self.assertEqual(resp.context['mentor'], self.post_data['mentor'])

    def test_email_already_exists(self):
        self.client.post(self.url, self.post_data)

        resp = self.client.post(self.url, self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup.html'))
        self.assertEqual(['email'], resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')
        self.assertEqual(len(mail.outbox), 1)  # One mail for first sucessful request

        self.assertEqual(resp.context['first_name'], self.post_data['first_name'])
        self.assertEqual(resp.context['last_name'], self.post_data['last_name'])
        self.assertEqual(resp.context['email'], self.post_data['email'])
        self.assertEqual(resp.context['address'], self.post_data['address'])
        self.assertEqual(resp.context['post'], self.post_data['post'])
        self.assertEqual(resp.context['school'], self.post_data['school'])
        self.assertEqual(resp.context['mentor'], self.post_data['mentor'])

    def test_deny_without_address(self):
        del self.post_data['address']
        resp = self.client.post(self.url, self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup.html'))
        self.assertEqual(['address'], resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')
        self.assertEqual(len(mail.outbox), 0)

        self.assertEqual(resp.context['first_name'], self.post_data['first_name'])
        self.assertEqual(resp.context['last_name'], self.post_data['last_name'])
        self.assertEqual(resp.context['email'], self.post_data['email'])
        self.assertEqual(resp.context['address'], '')
        self.assertEqual(resp.context['post'], self.post_data['post'])
        self.assertEqual(resp.context['school'], self.post_data['school'])
        self.assertEqual(resp.context['mentor'], self.post_data['mentor'])

    def test_deny_without_post(self):
        del self.post_data['post']
        resp = self.client.post(self.url, self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup.html'))
        self.assertEqual(['post'], resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')
        self.assertEqual(len(mail.outbox), 0)

        self.assertEqual(resp.context['first_name'], self.post_data['first_name'])
        self.assertEqual(resp.context['last_name'], self.post_data['last_name'])
        self.assertEqual(resp.context['email'], self.post_data['email'])
        self.assertEqual(resp.context['address'], self.post_data['address'])
        self.assertEqual(resp.context['post'], '')
        self.assertEqual(resp.context['school'], self.post_data['school'])
        self.assertEqual(resp.context['mentor'], self.post_data['mentor'])

    def test_deny_without_school(self):
        del self.post_data['school']
        resp = self.client.post(self.url, self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup.html'))
        self.assertEqual(['school'], resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')
        self.assertEqual(len(mail.outbox), 0)

        self.assertEqual(resp.context['first_name'], self.post_data['first_name'])
        self.assertEqual(resp.context['last_name'], self.post_data['last_name'])
        self.assertEqual(resp.context['email'], self.post_data['email'])
        self.assertEqual(resp.context['address'], self.post_data['address'])
        self.assertEqual(resp.context['post'], self.post_data['post'])
        self.assertEqual(resp.context['school'], '')
        self.assertEqual(resp.context['mentor'], self.post_data['mentor'])

    def test_deny_with_invalid_school(self):
        self.post_data['school'] = u'OŠ Spodnji Kašelj'
        resp = self.client.post(self.url, self.post_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup.html'))
        self.assertEqual(['school'], resp.context['errors'])
        self.assertNotEqual(resp.context['msg'], '')
        self.assertEqual(len(mail.outbox), 0)

        self.assertEqual(resp.context['first_name'], self.post_data['first_name'])
        self.assertEqual(resp.context['last_name'], self.post_data['last_name'])
        self.assertEqual(resp.context['email'], self.post_data['email'])
        self.assertEqual(resp.context['address'], self.post_data['address'])
        self.assertEqual(resp.context['post'], self.post_data['post'])
        self.assertEqual(resp.context['school'], self.post_data['school'])
        self.assertEqual(resp.context['mentor'], self.post_data['mentor'])

    def test_allow_without_mentor(self):
        del self.post_data['mentor']
        resp = self.client.post(self.url, self.post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, join('login', 'signup_confirm.html'))
        # self.assertEqual(len(mail.outbox), 1)

    def test_database(self):
        resp = self.client.post(self.url, self.post_data, follow=True)
        self.assertEqual(resp.status_code, 200)

        users = UserProfile.objects.all()  # plyint: disable=no-member
        self.assertEqual(len(users), 1)

        u = users[0]
        self.assertEqual(u.first_name, self.post_data['first_name'])
        self.assertEqual(u.last_name, self.post_data['last_name'])
        self.assertEqual(u.email, self.post_data['email'])
        self.assertEqual(u.school, self.post_data['school'])
        self.assertEqual(u.address, self.post_data['address'])
        self.assertEqual(u.post, self.post_data['post'])
        self.assertEqual(str(u.mentor), self.post_data['mentor'])


class FormsTestCase(TestCase):
    def setUp(self):
        mentor = Mentor.objects.create(name="Franc Horvat")
        self.user_data = {
            'first_name': "Janez",
            'last_name': "Novak",
            'mentor': mentor,
            'email': "janez.novak@example.com",
            'address': "Zgornji Kašelj 42",
            'post': "1234 Zgornji Kašelj",
            'school': "OS Zgornji Kašelj",
        }
        self.create_form = {
            'first_name': "Janez",
            'last_name': "Novak",
            'email': "janez.novak@example.com",
            'password1': 'test_pwd',
            'password2': 'test_pwd',
        }
        self.change_form = {
            'password1': 'new_pwd',
            'password2': 'new_pwd',
        }

    def test_valid_create_form(self):
        form = UserProfileCreationForm(data=self.create_form)
        self.assertEqual(form.is_valid(), True)  # pylint: disable=no-member

    def test_missmatching_create_passwords(self):
        self.create_form['password2'] = "wrong_pwd"
        form = UserProfileCreationForm(data=self.create_form)
        self.assertEqual(form.is_valid(), False)  # pylint: disable=no-member

    def test_existing_email(self):
        UserProfile.objects.create_user(**self.user_data)

        form = UserProfileCreationForm(data=self.create_form)
        self.assertEqual(form.is_valid(), False)  # pylint: disable=no-member

    # def test_valid_change_form(self):
    #     form = UserProfileChangeForm(data=self.change_form)
    #     self.assertEqual(form.is_valid(), True)

    # def test_missmatching_change_passwords(self):
    #     self.change_form['password2'] = "wrong_pwd"
    #     form = UserProfileChangeForm(data=self.change_form)
    #     self.assertEqual(form.is_valid(), False)


class UserProfileModelTestCase(TestCase):
    def setUp(self):
        mentor = Mentor.objects.create(name="Franc Horvat")
        self.user_data = {
            'first_name': "Janez",
            'last_name': "Novak",
            'mentor': mentor,
            'email': "janez.novak@example.com",
            'address': "Zgornji Kašelj 42",
            'post': "1234 Zgornji Kašelj",
            'school': "OS Zgornji Kašelj",
        }

        self.user = UserProfile.objects.create_user(**self.user_data)
        self.user.set_password('test_pwd')
        self.user.save()

    def test_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'Novak J.')

    def test_full_name(self):
        self.assertEqual(
            self.user.get_full_name(),
            '{} {}'.format(self.user_data['first_name'], self.user_data['last_name']))

    def test_unicode(self):
        self.assertEqual(
            unicode(self.user),
            '{} {}'.format(self.user_data['first_name'], self.user_data['last_name']))

    def test_send_email(self):
        self.user.email_user('Subject', 'Body')
        self.assertEqual(len(mail.outbox), 1)


class InstitutionModelTestCase(TestCase):
    def setUp(self):
        self.institution_data = {
            'name': u'OS Zgornji Kašelj'
        }

        self.institution = Institution.objects.create(**self.institution_data)

    def test_unicode(self):
        self.assertEqual(unicode(self.institution), self.institution_data['name'])
