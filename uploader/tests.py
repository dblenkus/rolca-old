# # pylint: disable=C0103,E1103

# from datetime import date, timedelta
# import os

# from django.test import TestCase
# from django.conf import settings
# from django.core.urlresolvers import reverse
# from django.core.files import File as djFile
# from tastypie.test import ResourceTestCase, TestApiClient

# from .models import File, Photo, Theme, Salon
# from login.models import Profile


# API_URL = '/api/v1/'
# TEST_IMG = [
#     os.path.join(settings.BASE_DIR, 'uploader', 'test_files', 'test_img.jpg'),
# ]


# def create_salon():
#     today = date.today()
#     day = timedelta(days=1)
#     return [
#         Salon.objects.create(title="Test salon", start_date=today - day,
#                              end_date=today + day, jury_date=today + 2 * day,
#                              results_date=today + 3 * day),
#         Salon.objects.create(title="Outdated salon", start_date=today - 4 * day,
#                              end_date=today - 3 * day, jury_date=today - 2 * day,
#                              results_date=today - day),
#         Salon.objects.create(title="Future salon", start_date=today + day,
#                              end_date=today + 2 * day, jury_date=today + 3 * day,
#                              results_date=today + 4 * day),
#     ]


# def create_theme(salon):
#     return [
#         Theme.objects.create(title='Nature', salon=salon[0], n_photos=1),
#         Theme.objects.create(title='Portrait', salon=salon[0], n_photos=1),
#     ]


# def create_file(user):
#     return [
#         File.objects.create(file=djFile(open(TEST_IMG[0], 'rb')), user=user[0]),
#     ]


# def create_user():
#     return [
#          Profile.objects.create_user(email="user@example.com",
#                                          password="test_pwd"),
#     ]


# def login(api_client):
#     return api_client.client.login(email="user@example.com", password="test_pwd")


# class DatabaseTestCase(TestCase):
#     def setUp(self):
#         pass

#     def test_file_model(self):
#         pass


# class UploaderTestCase(TestCase):
#     def setUp(self):
#         self.user = Profile.objects.create_user(email="test@blenkus.com",
#                                                     password="test_pwd")

#     def test_uploading_image(self):
#         self.client.login(email="test@blenkus.com", password="test_pwd")
#         with open(TEST_IMG[0], 'rb') as img:
#             self.client.post(reverse('upload'), {'files[]': img})
#         self.assertEqual(len(File.objects.all()), 1)

#     def test_unauthorized_image_upload(self):
#         with open(TEST_IMG[0], 'rb') as img:
#             resp = self.client.post(reverse('upload'), {'files[]': img})
#         self.assertEqual(resp.status_code, 403)
#         self.assertEqual(len(File.objects.all()), 0)

#     def test_upload_without_file(self):
#         resp = self.client.post('upload')
#         self.assertEqual(resp.status_code, 404)


# class BaseCheckMixin():
#     def test_get_list_unauthorized(self):
#         resp = self.api_client.get(self.url)
#         self.assertHttpUnauthorized(resp)

#     def test_get_unauthorized(self):
#         resp = self.api_client.get(self.detail_url)
#         self.assertHttpUnauthorized(resp)

#     def test_methods_not_allowed(self):
#         resp = self.api_client.post(self.detail_url, data=self.post_data)
#         self.assertHttpMethodNotAllowed(resp)


# class SalonResourceTest(ResourceTestCase, BaseCheckMixin):
#     def setUp(self):
#         super(SalonResourceTest, self).setUp()

#         create_user()
#         self.salon = create_salon()

#         self.url = '{0}salon/'.format(API_URL)
#         self.detail_url = '{0}{1}/'.format(self.url, self.salon[0].pk)

#         self.post_data = {
#             'title': 'Changed title'
#         }

#     def tearDown(self):
#         Photo.objects.all().delete()
#         File.objects.all().delete()
#         Theme.objects.all().delete()
#         Salon.objects.all().delete()
#         Profile.objects.all().delete()
#         super(SalonResourceTest, self).tearDown()

#     def test_dont_show_not_open_salons(self):
#         login(self.api_client)
#         resp = self.api_client.get(self.url)
#         self.assertHttpOK(resp)
#         salons = self.deserialize(resp)['objects']
#         self.assertEqual(len(salons), 1)
#         self.assertEqual(salons[0]['id'], self.salon[0].pk)

#     def test_show_salon_first_day(self):
#         self.salon[0].start_date = date.today()
#         self.salon[0].save()

#         login(self.api_client)
#         resp = self.api_client.get(self.url)
#         self.assertHttpOK(resp)
#         salons = self.deserialize(resp)['objects']
#         self.assertEqual(len(salons), 1)
#         self.assertEqual(salons[0]['id'], self.salon[0].pk)

#     def test_show_salon_last_day(self):
#         self.salon[0].end_date = date.today()
#         self.salon[0].save()

#         login(self.api_client)
#         resp = self.api_client.get(self.url)
#         self.assertHttpOK(resp)
#         salons = self.deserialize(resp)['objects']
#         self.assertEqual(len(salons), 1)
#         self.assertEqual(salons[0]['id'], self.salon[0].pk)


# class ThemeResourceTest(ResourceTestCase, BaseCheckMixin):
#     def setUp(self):
#         super(ThemeResourceTest, self).setUp()

#         salon = create_salon()
#         self.theme = create_theme(salon)

#         self.url = '{0}theme/'.format(API_URL)
#         self.detail_url = '{0}{1}/'.format(self.url, self.theme[0].pk)

#         self.post_data = {
#             'n_photos': 2
#         }

#     def tearDown(self):
#         Photo.objects.all().delete()
#         File.objects.all().delete()
#         Theme.objects.all().delete()
#         Salon.objects.all().delete()
#         Profile.objects.all().delete()
#         super(ThemeResourceTest, self).tearDown()


# class FileResourceTest(ResourceTestCase, BaseCheckMixin):
#     def setUp(self):
#         super(FileResourceTest, self).setUp()

#         user = create_user()
#         self.file = create_file(user)

#         self.url = '{0}file/'.format(API_URL)
#         self.detail_url = '{0}{1}/'.format(self.url, self.file[0].pk)

#         self.post_data = {
#             'file': 'other file'
#         }

#     def tearDown(self):
#         Photo.objects.all().delete()
#         File.objects.all().delete()
#         Theme.objects.all().delete()
#         Salon.objects.all().delete()
#         Profile.objects.all().delete()
#         super(FileResourceTest, self).tearDown()


# class PhotoResourceTest(ResourceTestCase):
#     fixtures = ['users', 'uploader']

#     def setUp(self):
#         super(PhotoResourceTest, self).setUp()

#         self.api_client = TestApiClient()

#     def tearDown(self):
#         Profile.objects.all().delete()
#         File.objects.all().delete()
#         Photo.objects.all().delete()
#         Theme.objects.all().delete()
#         Salon.objects.all().delete()
#         super(PhotoResourceTest, self).tearDown()

#     def test_get_list_unauthorized(self):
#         resp = self.api_client.get('/api/v1/photo/', format='json')
#         self.assertHttpUnauthorized(resp)

#     # def test_get_list(self):
#     #     self.api_client.client.login(email='user.one@example.com',
#     #                                  password='test_pwd')
#     #     resp = self.api_client.get('/api/v1/photo/', format='json')
#     #     self.assertValidJSONResponse(resp)
#     #     self.assertEqual(len(self.deserialize(resp)['objects']), 2)
