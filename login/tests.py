# -*- coding: utf-8 -*-
# pylint: disable=C0103,E1103
from __future__ import absolute_import, division, print_function, unicode_literals

import mock
import unittest

from django.test import RequestFactory, TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework.test import APITestCase


from .forms import ProfileCreationForm
from .models import Confirmation, Institution, Profile
from .views import login_view, logout_view, signup_view, _send_confirmation


# MESSAGES = {
#     u'NOT_FOUND': u'Not found.',
#     u'NO_PERMISSION': u'You do not have permission to perform this action.',
# }


class DatabaseTestCase(unittest.TestCase):
    def test_profile_full_name(self):
        profile = Profile(first_name="Janez", last_name="Novak")
        self.assertEqual(profile.get_full_name(), "Janez Novak")
        self.assertEqual(str(profile), "Janez Novak")

        profile = Profile(last_name="Novak")
        self.assertEqual(profile.get_full_name(), "Novak")
        self.assertEqual(str(profile), "Novak")

        profile = Profile(first_name="Janez")
        self.assertEqual(profile.get_full_name(), "Janez")
        self.assertEqual(str(profile), "Janez")

    def test_profile_short_name(self):
        profile = Profile(first_name="Janez", last_name="Novak")
        self.assertEqual(profile.get_short_name(), "Novak J.")

        profile = Profile(last_name="Novak")
        self.assertEqual(profile.get_short_name(), "Novak")

        profile = Profile(first_name="Janez")
        self.assertEqual(profile.get_short_name(), "J.")

    def test_institutuion_str(self):
        institution = Institution(name="Test institution")
        self.assertEqual(str(institution), "Test institution")


class LoginTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = RequestFactory()

        cls.url_index = reverse('index')
        cls.url_login = reverse('login')
        cls.url_logout = reverse('logout')
        cls.url_upload_app = reverse('upload_app')

        cls.post_data = {'email': 'user@example.com', 'password': 'test_pwd'}

    @mock.patch('login.views.login')
    @mock.patch('login.views.authenticate')
    def test_login_successful(self, authenticate_mock, login_mock):
        user = mock.Mock()
        authenticate_mock.return_value = user

        request = self.factory.post(self.url_login, self.post_data)
        resp = login_view(request)

        login_mock.assert_called_once_with(request, user)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.get('location'), self.url_upload_app)

    @mock.patch('login.views.render')
    @mock.patch('login.views.login')
    @mock.patch('login.views.authenticate')
    def test_login_not_active(self, authenticate_mock, login_mock, render_mock):
        authenticate_mock.return_value = mock.Mock(is_active=False)
        render_mock.side_effect = lambda req, temp, resp: HttpResponse(resp['msg'])

        request = self.factory.post(self.url_login, self.post_data)
        resp = login_view(request)

        login_mock.assert_not_called()
        self.assertEqual(resp.content, b"Vaš račun je bil onemogočen.")

    @mock.patch('login.views.render')
    @mock.patch('login.views.login')
    def test_login_missing_email(self, login_mock, render_mock):
        render_mock.side_effect = lambda req, temp, resp: HttpResponse(resp['msg'])

        post_data = self.post_data.copy()
        del post_data['email']
        request = self.factory.post(self.url_login, post_data)
        resp = login_view(request)

        login_mock.assert_not_called()
        self.assertEqual(resp.content, b"Prosim vpišite email naslov.")

    @mock.patch('login.views.render')
    @mock.patch('login.views.login')
    def test_login_missing_password(self, login_mock, render_mock):
        render_mock.side_effect = lambda req, temp, resp: HttpResponse(resp['msg'])

        post_data = self.post_data.copy()
        del post_data['password']
        request = self.factory.post(self.url_login, post_data)
        resp = login_view(request)

        login_mock.assert_not_called()
        self.assertEqual(resp.content, b"Prosim vpišite geslo.")

    @mock.patch('login.views.render')
    @mock.patch('login.views.login')
    def test_login_missing_all(self, login_mock, render_mock):
        render_mock.side_effect = lambda req, temp, resp: HttpResponse(resp['msg'])

        request = self.factory.post(self.url_login, {})
        resp = login_view(request)

        login_mock.assert_not_called()
        self.assertEqual(resp.content, b"Prosim vpišite email naslov.")

    @mock.patch('login.views.render')
    @mock.patch('login.views.login')
    @mock.patch('login.views.authenticate')
    def test_login_wrong_password(self, authenticate_mock, login_mock, render_mock):
        authenticate_mock.return_value = None
        render_mock.side_effect = lambda req, temp, resp: HttpResponse(resp['msg'])

        request = self.factory.post(self.url_login, self.post_data)
        resp = login_view(request)

        login_mock.assert_not_called()
        self.assertEqual(resp.content, b"Email naslov in geslo se ne ujemata.")

        print(render_mock.call_args)

    @mock.patch('login.views.logout')
    def test_logout(self, logout_mock):
        request = self.factory.get(self.url_logout)
        resp = logout_view(request)

        logout_mock.assert_called_once_with(request)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.get('location'), self.url_index)


class SignupTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = RequestFactory()

        cls.post_data = {
            'first_name': 'Janez',
            'last_name': 'Novak',
            'email': 'janez.novak@example.com',
            'address': 'Zgornji Kašelj 42',
            'post': '1234 Zgornji Kašelj',
            'school': 'OS Zgornji Kašelj',
        }

        cls.url_signup = reverse('signup')

    @mock.patch('login.views._send_confirmation')
    @mock.patch('login.views.Institution.objects.filter')
    @mock.patch('login.views.Profile.objects')
    def test__successful(self, profile_mock, institution_mock, confirmation_mock):
        institution_mock.return_value = mock.Mock(exists=lambda: True)
        profile_mock.filter.return_value = mock.Mock(exists=lambda: False)
        profile_mock.make_random_password.return_value = 'test_pwd'

        request = self.factory.post(self.url_signup, self.post_data)
        signup_view(request)

        profile_mock.create_user.assert_called_once_with(
            password='test_pwd', **self.post_data)

    @mock.patch('login.views.render')
    @mock.patch('login.views.Institution.objects.filter')
    @mock.patch('login.views.Profile.objects')
    def test_already_exists(self, profile_mock, institution_mock, render_mock):
        institution_mock.return_value = mock.Mock(exists=lambda: True)
        profile_mock.filter.return_value = mock.Mock(exists=lambda: True)

        request = self.factory.post(self.url_signup, self.post_data)
        signup_view(request)

        self.assertFalse(profile_mock.create_user.called)

    @mock.patch('login.views.render')
    @mock.patch('login.views.Institution.objects.filter')
    @mock.patch('login.views.Profile.objects')
    def test_nonexisting_school(self, profile_mock, institution_mock, render_mock):
        institution_mock.return_value = mock.Mock(exists=lambda: False)
        profile_mock.filter.return_value = mock.Mock(exists=lambda: False)

        request = self.factory.post(self.url_signup, self.post_data)
        signup_view(request)

        self.assertFalse(profile_mock.create_user.called)

    @mock.patch('login.views.render')
    @mock.patch('login.views.Institution.objects.filter')
    @mock.patch('login.views.Profile.objects')
    def test_missing_parameter(self, profile_mock, institution_mock, render_mock):
        institution_mock.return_value = mock.Mock(exists=lambda: True)
        profile_mock.filter.return_value = mock.Mock(exists=lambda: False)

        def _witout_parameter(parameter):
            post_data = self.post_data.copy()
            del post_data[parameter]
            request = self.factory.post(self.url_signup, post_data)
            signup_view(request)

            self.assertFalse(profile_mock.create_user.called)

        _witout_parameter('first_name')
        _witout_parameter('last_name')
        _witout_parameter('email')
        _witout_parameter('address')
        _witout_parameter('post')
        _witout_parameter('school')

    @mock.patch('login.views.get_template')
    @mock.patch('login.views.get_current_site')
    def test_user_activation(self, current_site_mock, get_template_mock):
        current_site_mock.domain = 'example.com'
        current_site_mock.name = 'Test site'
        user_mock = mock.Mock(spec=Profile, email='user@example.com')
        user_mock.get_token.return_value = 'test_token'

        request = self.factory.post(self.url_signup, self.post_data)

        _send_confirmation(request, user_mock, 'test_pwd')

        self.assertTrue(user_mock.email_user.called)


# class SignupTestCaseOld(TestCase):
#     def setUp(self):
#         Institution.objects.create(name=u'OS Zgornji Kašelj')

#         self.post_data = {
#             u'first_name': u'Janez',
#             u'last_name': u'Novak',
#             u'email': u'janez.novak@example.com',
#             u'address': u'Zgornji Kašelj 42',
#             u'post': u'1234 Zgornji Kašelj',
#             u'school': u'OS Zgornji Kašelj',

#         }

#         self.url = reverse('signup')

#     def test_invalid_activation_token(self):
#         bad_token = "1" * 32

#         user = Profile.objects.create(**self.post_data)
#         uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

#         resp = self.client.get(reverse('signup_activation',
#                                        kwargs={'uidb64': uidb64, 'token': bad_token}),
#                                follow=True)
#         self.assertEqual(resp.status_code, 200)
#         self.assertTemplateUsed(resp, join('login', 'activation_bad.html'))

#         user.refresh_from_db()
#         self.assertFalse(user.is_active)


# class FormsTestCase(TestCase):
#     def setUp(self):
#         self.user_data = {
#             'first_name': "Janez",
#             'last_name': "Novak",
#             'email': "janez.novak@example.com",
#             'address': "Zgornji Kašelj 42",
#             'post': "1234 Zgornji Kašelj",
#             'school': "OS Zgornji Kašelj",
#         }
#         self.create_form = {
#             'first_name': "Janez",
#             'last_name': "Novak",
#             'email': "janez.novak@example.com",
#             'password1': 'test_pwd',
#             'password2': 'test_pwd',
#         }
#         self.change_form = {
#             'password1': 'new_pwd',
#             'password2': 'new_pwd',
#         }

#     def test_valid_create_form(self):
#         form = ProfileCreationForm(data=self.create_form)
#         self.assertEqual(form.is_valid(), True)  # pylint: disable=no-member

#     def test_missmatching_create_passwords(self):
#         self.create_form['password2'] = "wrong_pwd"
#         form = ProfileCreationForm(data=self.create_form)
#         self.assertEqual(form.is_valid(), False)  # pylint: disable=no-member

#     def test_existing_email(self):
#         Profile.objects.create_user(**self.user_data)

#         form = ProfileCreationForm(data=self.create_form)
#         self.assertEqual(form.is_valid(), False)  # pylint: disable=no-member

    # def test_valid_change_form(self):
    #     form = ProfileChangeForm(data=self.change_form)
    #     self.assertEqual(form.is_valid(), True)

    # def test_missmatching_change_passwords(self):
    #     self.change_form['password2'] = "wrong_pwd"
    #     form = ProfileChangeForm(data=self.change_form)
    #     self.assertEqual(form.is_valid(), False)


# class ProfileModelTestCase(TestCase):
#     def setUp(self):
#         self.user_data = {
#             'first_name': "Janez",
#             'last_name': "Novak",
#             'email': "janez.novak@example.com",
#             'address': "Zgornji Kašelj 42",
#             'post': "1234 Zgornji Kašelj",
#             'school': "OS Zgornji Kašelj",
#         }

#         self.user = Profile.objects.create_user(**self.user_data)
#         self.user.set_password('test_pwd')
#         self.user.save()

#     def test_short_name(self):
#         self.assertEqual(self.user.get_short_name(), 'Novak J.')

#     def test_full_name(self):
#         self.assertEqual(
#             self.user.get_full_name(),
#             '{} {}'.format(self.user_data['first_name'], self.user_data['last_name']))

#     def test_unicode(self):
#         self.assertEqual(
#             unicode(self.user),
#             '{} {}'.format(self.user_data['first_name'], self.user_data['last_name']))


# class ProfileAPITestCase(APITestCase):  # pylint: disable=too-many-instance-attributes
#     fixtures = ['profiles.yaml']

#     def setUp(self):
#         super(ProfileAPITestCase, self).setUp()

#         self.factory = APIRequestFactory()

#         self.user1 = Profile.objects.get(pk=1)
#         self.user2 = Profile.objects.get(pk=2)

#         self.list_view = ProfileViewSet.as_view({
#             'get': 'list',
#             'post': 'create',
#         })
#         self.list_url = reverse('rolca-api:user-list')

#         self.detail_view = ProfileViewSet.as_view({
#             'get': 'retrieve',
#             'put': 'update',
#             'patch': 'partial_update',
#             'delete': 'destroy',
#         })
#         self.detail_url = reverse('rolca-api:user-detail', kwargs={'pk': 1})

#         self.data = {'first_name': 'Osama', 'last_name': 'Bin Laden'}

#     def _get_list(self, user=None):
#         request = self.factory.get(self.list_url)
#         if user:
#             force_authenticate(request, user)
#         resp = self.list_view(request)
#         resp.render()
#         return resp

#     def _post(self, data, user=None):
#         request = self.factory.post(self.list_url, data=data)
#         if user:
#             force_authenticate(request, user)
#         resp = self.list_view(request)
#         resp.render()
#         return resp

#     def _get_detail(self, pk, user=None):
#         request = self.factory.get(self.detail_url)
#         if user:
#             force_authenticate(request, user)
#         resp = self.detail_view(request, pk=pk)
#         resp.render()
#         return resp

#     def _put(self, pk, data, user=None):
#         request = self.factory.put(self.detail_url, data=data)
#         if user:
#             force_authenticate(request, user)
#         resp = self.detail_view(request, pk=pk)
#         resp.render()
#         return resp

#     def _patch(self, pk, data, user=None):
#         request = self.factory.patch(self.detail_url, data=data)
#         if user:
#             force_authenticate(request, user)
#         resp = self.detail_view(request, pk=pk)
#         resp.render()
#         return resp

#     def _delete(self, pk, user=None):
#         request = self.factory.delete(self.detail_url)
#         if user:
#             force_authenticate(request, user)
#         resp = self.detail_view(request, pk=pk)
#         resp.render()
#         return resp

#     def test_get_list(self):
#         # public user
#         resp = self._get_list()
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(len(resp.data), 0)

#         # normal user
#         resp = self._get_list(self.user1)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(len(resp.data), 1)

#         # mentor
#         resp = self._get_list(self.user2)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(len(resp.data), 2)

#     def test_post(self):
#         # public user
#         resp = self._post(self.data)
#         self.assertEqual(resp.status_code, 404)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NOT_FOUND'])

#         # normal user
#         resp = self._post(self.data, self.user1)
#         self.assertEqual(resp.status_code, 403)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NO_PERMISSION'])

#         # mentor
#         resp = self._post(self.data, self.user2)
#         self.assertEqual(resp.status_code, 201)

#     def test_get_detail(self):
#         # public user
#         resp = self._get_detail(1)
#         self.assertEqual(resp.status_code, 404)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NOT_FOUND'])

#         # normal user
#         resp = self._get_detail(1, self.user1)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(resp.data[u'id'], 1)
#         resp = self._get_detail(2, self.user1)
#         self.assertEqual(resp.status_code, 404)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NOT_FOUND'])

#         # mentor
#         resp = self._get_detail(1, self.user2)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(resp.data[u'id'], 1)
#         resp = self._get_detail(2, self.user2)
#         self.assertEqual(resp.status_code, 200)
#         self.assertEqual(resp.data[u'id'], 2)

#     def test_put(self):
#         # public user
#         resp = self._put(1, self.data)
#         self.assertEqual(resp.status_code, 404)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NOT_FOUND'])

#         # normal user
#         resp = self._put(1, self.data, self.user1)
#         self.assertEqual(resp.status_code, 403)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NO_PERMISSION'])

#         # mentor
#         resp = self._put(1, self.data, self.user2)
#         self.assertEqual(resp.status_code, 200)

#     def test_patch(self):
#         # public user
#         resp = self._patch(1, self.data)
#         self.assertEqual(resp.status_code, 404)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NOT_FOUND'])

#         # normal user
#         resp = self._patch(1, self.data, self.user1)
#         self.assertEqual(resp.status_code, 403)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NO_PERMISSION'])

#         # mentor
#         resp = self._patch(1, self.data, self.user2)
#         self.assertEqual(resp.status_code, 200)

#     def test_delete(self):
#         # public user
#         resp = self._delete(1)
#         self.assertEqual(resp.status_code, 404)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NOT_FOUND'])

#         # normal user
#         resp = self._delete(1, self.user1)
#         self.assertEqual(resp.status_code, 403)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NO_PERMISSION'])

#         # mentor
#         resp = self._delete(1, self.user2)
#         self.assertEqual(resp.status_code, 204)
#         resp = self._delete(2, self.user2)
#         self.assertEqual(resp.status_code, 403)
#         self.assertEqual(resp.data[u'detail'], MESSAGES['NO_PERMISSION'])


# class InstitutionModelTestCase(TestCase):
#     def setUp(self):
#         self.institution_data = {
#             'name': u'OS Zgornji Kašelj'
#         }

#         self.institution = Institution.objects.create(**self.institution_data)

#     def test_unicode(self):
#         self.assertEqual(unicode(self.institution), self.institution_data['name'])


# class InstitutionAPITestCase(APITestCase):
#     pass


# class ConfirmationModelTestCase(TestCase):
#     def setUp(self):
#         user_data = {
#             'first_name': "Janez",
#             'last_name': "Novak",
#             'email': "janez.novak@example.com",
#             'address': "Zgornji Kašelj 42",
#             'post': "1234 Zgornji Kašelj",
#             'school': "OS Zgornji Kašelj",
#         }
#         user = Profile.objects.create(**user_data)

#         self.confirmation_data = {
#             'profile': user,
#             'token': '123',
#         }
#         self.conf = Confirmation.objects.create(**self.confirmation_data)

#     def test_unicode(self):
#         self.assertEqual(unicode(self.conf), "uid:1 token:123")
