from django.conf.urls import patterns, include, url
from django.conf import settings
from rest_framework import routers
from user2 import views

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthentificationForm


from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'wines', views.WineViewSet)
router.register(r'movements', views.MovementViewSet)
router.register(r'containers', views.ContainerViewSet)
router.register(r'bottles', views.BottleViewSet)
#router.register(r'vinibar', views.VinibarView, base_name='vinibar')
router.register(r'vinibar', views.VinibarViewSet, base_name='vinibar')
router.register(r'vinibarwines', views.VinibarWinesViewSet, base_name='vinibarwines')
router.register(r'ratedwines', views.RatedWinesViewSet, base_name='ratedwines')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^login/$', views.login, name='login'),
    url(r'^login/?$','django.contrib.auth.views.login',{'template_name':'/static/login.html', 'authentication_form':AuthenticationForm}),
    # url(r'^$', 'usertest2.views.home', name='home'),
    # url(r'^usertest2/', include('usertest2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}), #added for heroku
)

urlpatterns += patterns('',
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token')
)
# urlpatterns = format_suffix_patterns(urlpatterns)