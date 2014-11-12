from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

import snotes20.views as views

router = routers.DefaultRouter()

router.register(r'auth', views.AuthViewSet, base_name='auth')
router.register(r'users', views.UserViewSet, base_name='users')
router.register(r'soonepisodes', views.SoonEpisodeViewSet, base_name='sonnepisodes')
router.register(r'documents', views.DocumentViewSet, base_name='documents')
router.register(r'importerlogs', views.ImporterLogViewSet, base_name='importerlogs')
router.register(r'editors', views.EditorViewSet, base_name='editors')
router.register(r'archive', views.ArchiveViewSet, base_name='archive')
router.register(r'podcasts', views.PodcastViewSet, base_name='podcasts')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

if settings.DEBUG:
    urlpatterns += static('media', document_root=settings.MEDIA_ROOT)
