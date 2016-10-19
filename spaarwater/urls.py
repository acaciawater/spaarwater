"""spaarwater URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from views import HomeView, DashGroupView, OverviewView
from pictures import PFDripView, PFRefView, InfiltratieView, OpslagView

urlpatterns = [url(r'^$', HomeView.as_view(), name='home'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^data/', include('acacia.data.urls', namespace='acacia')),
    url(r'^view/(?P<pk>\d+)$', OverviewView.as_view(), name='overview'),
    url(r'^pfdrip/(?P<pk>\d+)$', PFDripView.as_view()),
    url(r'^pfref/(?P<pk>\d+)$', PFRefView.as_view()),
    url(r'^infiltratie/(?P<pk>\d+)$', InfiltratieView.as_view()),
    url(r'^opslag/(?P<pk>\d+)$', OpslagView.as_view()),

    url(r'^(?P<name>\w+)$', DashGroupView.as_view(), name='spaarwater-dashboard'),
    url(r'^chaining/', include('smart_selects.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.IMG_URL, document_root=settings.IMG_ROOT)

from django.contrib.auth import views as auth_views
urlpatterns += [url(r'^password/change/$',
                    auth_views.password_change,
                    name='password_change'),
    url(r'^password/change/done/$',
                    auth_views.password_change_done,
                    name='password_change_done'),
    url(r'^password/reset/$',
                    auth_views.password_reset,
                    name='password_reset'),
    url(r'^accounts/password/reset/done/$',
                    auth_views.password_reset_done,
                    name='password_reset_done'),
    url(r'^password/reset/complete/$',
                    auth_views.password_reset_complete,
                    name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                    auth_views.password_reset_confirm,
                    name='password_reset_confirm'),
    url(r'^accounts/', include('registration.backends.default.urls'))    
]
