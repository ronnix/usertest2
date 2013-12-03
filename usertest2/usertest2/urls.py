from django.conf.urls import patterns, include, url
from rest_framework import routers
from user2 import views

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'wines', views.WineViewSet)
router.register(r'movements', views.MovementViewSet)
router.register(r'containers', views.ContainerViewSet)


urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', 'usertest2.views.home', name='home'),
    # url(r'^usertest2/', include('usertest2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
