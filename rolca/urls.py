from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
# from django.views.generic import RedirectView

from rest_framework import routers

from login.views import ProfileViewSet, InstitutionViewSet
from uploader.api import PhotoViewSet, SalonViewSet
from jury.api import RatingViewSet
# from login.api import ProfileResource, InstitutionResource
# from uploader.api import PhotoResource, SalonResource, ThemeResource, FileResource


router = routers.DefaultRouter()
router.register(r'user', ProfileViewSet)
router.register(r'school', InstitutionViewSet)
router.register(r'salon', SalonViewSet)
router.register(r'photo', PhotoViewSet)
router.register(r'rating', RatingViewSet)

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/v1/', include(router.urls)),
    url(r'^delavnice/', include('workshops.urls')),
    url(r'^rezultati/', include('results.urls')),
    url(r'^upload/', include('uploader.urls')),
    url(r'^uporabnik/', include('login.urls')),
    url(r'^natecaji/', include('uploader.urls')),
    url(r'^zirija/', include('jury.urls')),

    # url(r'^$', RedirectView.as_view(url='/upload/'), name="index")
    url(r'^', include('frontend.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
