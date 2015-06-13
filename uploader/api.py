from datetime import date

# from tastypie.resources import ModelResource
# from tastypie.authentication import SessionAuthentication
# from tastypie.authorization import Authorization, ReadOnlyAuthorization
# from tastypie import fields

from rest_framework import viewsets, serializers

from .models import File, Photo, Salon, Theme


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file',)


class PhotoSerializer(serializers.ModelSerializer):
    photo = FileSerializer()

    class Meta:
        model = Photo
        exclude = ('user', 'theme')


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        queryset = super(PhotoViewSet, self).get_queryset()
        salon = Salon.objects.filter(judges=self.request.user)[0]
        theme = Theme.objects.filter(salon=salon)[0]
        return queryset.filter(theme=theme)


class SalonViewSet(viewsets.ModelViewSet):
    queryset = Salon.objects.filter(end_date__gte=date.today(),
                                    start_date__lte=date.today())
    serializer_class = SalonSerializer


# class UserObjectsOnlyAuthorization(Authorization):
#     """Custom authorization class
#
#     Loged-in user can create objects, but can only access and edit
#     objects created by them.
#
#     """
#
#     def read_list(self, object_list, bundle):
#         """Users can get objects created by them."""
#         return object_list.filter(user=bundle.request.user)
#
#     def read_detail(self, object_list, bundle):
#         """Users can get objects created by them."""
#         return bundle.obj.user == bundle.request.user
#
#     def create_list(self, object_list, bundle):
#         """Users can create anything."""
#         return object_list
#
#     def create_detail(self, object_list, bundle):
#         """Users can create anything."""
#         return object_list
#
#     def update_list(self, object_list, bundle):
#         """Users can update objects created by them."""
#         allowed = []
#         for obj in object_list:
#             if obj.user == bundle.request.user:
#                 allowed.append(obj)
#
#         return allowed
#
#     def update_detail(self, object_list, bundle):
#         """Users can update objects created by them."""
#         return bundle.obj.user == bundle.request.user
#
#     def delete_list(self, object_list, bundle):
#         """Users can delete objects created by them."""
#         allowed = []
#         for obj in object_list:
#             if obj.user == bundle.request.user:
#                 allowed.append(obj)
#
#         return allowed
#
#     def delete_detail(self, object_list, bundle):
#         """Users can delete objects created by them."""
#         return bundle.obj.user == bundle.request.user
#
#
# class ThemeResource(ModelResource):
#     salon = fields.ToOneField('uploader.api.SalonResource', 'salon')
#
#     class Meta:
#         queryset = Theme.objects.all()
#         resource_name = 'theme'
#         allowed_methods = ['get']
#         authentication = SessionAuthentication()
#         authorization = ReadOnlyAuthorization()
#
#
# class SalonResource(ModelResource):
#     themes = fields.ToManyField(ThemeResource, 'theme_set', full=True)
#     judges = fields.ToManyField(ProfileResource, 'judges', full=True)
#
#     class Meta:
#         queryset = Salon.objects.filter(end_date__gte=date.today(),
#                                         start_date__lte=date.today())
#         resource_name = 'salon'
#         allowed_methods = ['get']
#         authentication = SessionAuthentication()
#         authorization = ReadOnlyAuthorization()
#
#
# class FileResource(ModelResource):
#     class Meta:
#         queryset = File.objects.all()
#         resource_name = 'file'
#         allowed_methods = ['get']
#         authentication = SessionAuthentication()
#         authorization = UserObjectsOnlyAuthorization()
#
#
# class PhotoResource(ModelResource):
#     # theme = fields.ToOneField(ThemeResource, 'theme', full=True)
#     # user = fields.ToOneField(ProfileResource, 'user', full=True)
#     # photo = fields.ToOneField(FileResource, 'photo', full=True)
#
#     def obj_create(self, bundle, **kwargs):
#         return super(PhotoResource, self).obj_create(bundle=bundle, **kwargs)
#
#     class Meta:
#         queryset = Photo.objects.all()
#         resource_name = 'photo'
#         authorization = Authorization()
#         allowed_methods = ['get', 'post']
#         # authentication = SessionAuthentication()
#         # authorization = UserObjectsOnlyAuthorization()
