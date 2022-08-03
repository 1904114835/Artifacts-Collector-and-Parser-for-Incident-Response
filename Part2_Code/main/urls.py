from django.urls import path

from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import cache_control
from django.conf import settings

# add --nostatic after manage.py runserver to disable static files

from . import views
from .models import *

type_of_artifacts = [BasicInfor,
                    EvtxApplication,
                    EvtxAppxOperational,
                    EvtxGrouppolicyOperational,
                    EvtxNtfsOperational,
                    EvtxPowershellOperational,
                    EvtxSecurity,
                    EvtxStoreOperational,
                    EvtxSystem,
                    EvtxWindowsPowershell,
                    Iconcache,
                    Jumplist,
                    Lnk,
                    Prefetch,
                    RecycleBin,
                    RegistryAutorun,
                    RegistryConnDevice,
                    RegistryUsbname,
                    RegistryUserassist,
                    RegistryWireless,
                    Win10Activity,
                    Win10Packageid,]

urlpatterns = [
    path('', views.index, name='index'),
    path('iconcache/', views.iconcache, name='activity_iconcache'),
    path('basicinfor/', views.basicinfor, name='activity_basicinfor'),
    path('eventlog/', views.eventlog, name='activity_eventlog'),
    path('registryautorun/', views.registryautorun, name='activity_registryautorun'),
    path('item/<str:event>/<str:idx>', views.item, name='item'),
    path('piechart/', views.piechart, name='piechart'),
    path('barchart/', views.barchart, name='barchart'),
    path('analysis/', views.analysis, name='analysis'),
    path('aboutus/', views.about_us, name='aboutus'),
    path('devicelist/', views.device_list, name='device_list'),
    path('test/', views.test, name='test'),
    path('detector/', views.detector, name='detector'),
]

for artifact_cls in type_of_artifacts:
    urlpatterns.append(path('blog/{}/'.format(artifact_cls.__name__.lower()), views.blog, name='blog_{}'.format(artifact_cls.__name__.lower())))


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, view=cache_control(no_cache=True, must_revalidate=True)(serve))