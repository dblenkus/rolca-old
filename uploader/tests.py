from __future__ import absolute_import, division, print_function, unicode_literals

from datetime import date, timedelta
import mock
import unittest

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from .models import File, Participent, Photo, Salon, Theme
from .views import PhotoViewSet, SalonViewSet


class DatabaseTestCase(unittest.TestCase):
    def test_salon_str(self):
        salon = Salon(title="Test salon")
        self.assertEqual(str(salon), "Test salon")

    def test_salon_active(self):
        salon = Salon()
        today = date.today()
        day = timedelta(days=1)

        # active salon
        salon.start_date = today - day
        salon.end_date = today + day
        self.assertTrue(salon.is_active())

        # past salon
        salon.start_date = today - 2 * day
        salon.end_date = today - day
        self.assertFalse(salon.is_active())

        # future salon
        salon.start_date = today + day
        salon.end_date = today + 2 * day
        self.assertFalse(salon.is_active())

    def test_theme_str(self):
        theme = Theme(title="Test theme")
        self.assertEqual(str(theme), "Test theme")

    def test_file_str(self):
        # TODO
        pass

    def test_participant_str(self):
        participent = Participent(first_name="Janez", last_name="Novak")
        self.assertEqual(str(participent), "Janez Novak")

    def test_photo_str(self):
        photo = Photo(title="Test photo")
        self.assertEqual(str(photo), "Test photo")


class DjangoDatabaseTestCase(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user1 = user_model.objects.create_user(
            'user1@example.com', 'test_pwd1', username='user1')
        self.user2 = user_model.objects.create_user(
            'user2@example.com', 'test_pwd2', username='user2')
        self.judge = user_model.objects.create_user(
            'user3@example.com', 'test_pwd3')

        today = date.today()
        self.salon = Salon.objects.create(
            owner=self.judge,
            title='Test salon',
            start_date=today,
            end_date=today,
            jury_date=today + timedelta(days=1),
            results_date=today + timedelta(days=2))
        self.salon.judges.add(self.judge)

        theme = Theme.objects.create(title='Test theme', salon=self.salon, n_photos=2)

        participent1 = Participent.objects.create(uploader=self.user1)
        participent2 = Participent.objects.create(uploader=self.user2)

        file1 = File.objects.create(user=self.user1)
        file2 = File.objects.create(user=self.user2)
        file3 = File.objects.create(user=self.user2)

        Photo.objects.create(
            title="Photo 1", participent=participent1, theme=theme, photo=file1)
        Photo.objects.create(
            title="Photo 2", participent=participent2, theme=theme, photo=file2)
        Photo.objects.create(
            title="Photo 3", participent=participent2, theme=theme, photo=file3)

    def test_photo_queryset(self):
        viewset_mock = mock.Mock(spec=PhotoViewSet)

        viewset_mock.request = mock.Mock(user=self.user2)
        self.assertEqual(len(PhotoViewSet.get_queryset(viewset_mock)), 2)

        viewset_mock.request = mock.Mock(user=self.judge)
        self.assertEqual(len(PhotoViewSet.get_queryset(viewset_mock)), 3)

        self.salon.results_date = date.today() - timedelta(days=1)
        self.salon.save()

        viewset_mock.request = mock.Mock(user=self.user2)
        self.assertEqual(len(PhotoViewSet.get_queryset(viewset_mock)), 3)


class SalonApiTestCase(APITestCase):
    def setUp(cls):
        cls.factory = APIRequestFactory()

        cls.salon_list_view = SalonViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
        cls.list_url = reverse('rolca-api:salon-list')
        cls.salon_detail_view = SalonViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })
        cls.detail_url = lambda pk: reverse('rolca-api:salon-detail', kwargs={'pk': pk})

    @mock.patch('uploader.views.SalonViewSet.create')
    def test_create_perms(self, salon_create_mock):
        salon_create_mock.return_value = Response('Dummy response', status=201)
        request = self.factory.post(self.list_url, {}, format='json')

        # public user
        resp = self.salon_list_view(request)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_create_mock.call_count, 0)

        # normal user
        user = mock.MagicMock(spec=get_user_model(), is_superuser=False, is_staff=False)
        force_authenticate(request, user)
        resp = self.salon_list_view(request)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_create_mock.call_count, 0)

        # admin user
        user.is_superuser = True
        user.is_staff = True
        resp = self.salon_list_view(request)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(salon_create_mock.call_count, 1)

    @mock.patch('uploader.views.SalonViewSet.list')
    def test_get_list_perms(self, salon_list_mock):
        salon_list_mock.return_value = Response('Dummy response')

        request = self.factory.get(self.list_url, format='json')

        # public user
        resp = self.salon_list_view(request)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(salon_list_mock.call_count, 1)
        salon_list_mock.reset_mock()

        # normal user
        user = mock.MagicMock(spec=get_user_model(), is_superuser=False, is_staff=False)
        force_authenticate(request, user)
        resp = self.salon_list_view(request)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(salon_list_mock.call_count, 1)

    @mock.patch('uploader.views.SalonViewSet.retrieve')
    def test_get_detail_perms(self, salon_retrieve_mock):
        salon_retrieve_mock.return_value = Response('Dummy response')

        request = self.factory.get(self.detail_url(1), format='json')

        # public user
        resp = self.salon_detail_view(request)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(salon_retrieve_mock.call_count, 1)
        salon_retrieve_mock.reset_mock()

        # normal user
        user = mock.MagicMock(spec=get_user_model(), is_superuser=False, is_staff=False)
        force_authenticate(request, user)
        resp = self.salon_detail_view(request)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(salon_retrieve_mock.call_count, 1)

    @mock.patch('uploader.views.SalonViewSet.update')
    def test_put_perms(self, salon_update_mock):
        salon_update_mock.return_value = Response('Dummy response')

        request = self.factory.put(self.detail_url(1), {}, format='json')

        # public user
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_update_mock.call_count, 0)

        # normal user
        user = mock.MagicMock(spec=get_user_model(), is_superuser=False, is_staff=False)
        force_authenticate(request, user)
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_update_mock.call_count, 0)

        # admin user
        user.is_superuser = True
        user.is_staff = True
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(salon_update_mock.call_count, 1)

    @mock.patch('uploader.views.SalonViewSet.partial_update')
    def test_patch_perms(self, salon_update_mock):
        salon_update_mock.return_value = Response('Dummy response')

        request = self.factory.patch(self.detail_url(1), {}, format='json')

        # public user
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_update_mock.call_count, 0)

        # normal user
        user = mock.MagicMock(spec=get_user_model(), is_superuser=False, is_staff=False)
        force_authenticate(request, user)
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_update_mock.call_count, 0)

        # admin user
        user.is_superuser = True
        user.is_staff = True
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(salon_update_mock.call_count, 1)

    @mock.patch('uploader.views.SalonViewSet.destroy')
    def test_delete_perms(self, salon_update_mock):
        salon_update_mock.return_value = Response('Dummy response')

        request = self.factory.delete(self.detail_url(1), {}, format='json')

        # public user
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_update_mock.call_count, 0)

        # normal user
        user = mock.MagicMock(spec=get_user_model(), is_superuser=False, is_staff=False)
        force_authenticate(request, user)
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(salon_update_mock.call_count, 0)

        # admin user
        user.is_superuser = True
        user.is_staff = True
        resp = self.salon_detail_view(request, pk=1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(salon_update_mock.call_count, 1)


class UploaderIntegrationTestCase(APITestCase):
    pass
