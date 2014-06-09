from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import viewsets, routers

#class UserViewSet(viewsets.ModelViewSet):
#    model = User

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)



urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
