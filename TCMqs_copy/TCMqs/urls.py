"""TCMqs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from . import  settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'tinymce/', include('tinymce.urls')),
    re_path(r'^user/', include(("apps.user.urls",'apps.user'),namespace='user')),
    re_path(r'^video/', include(('apps.video.urls','apps.video'),namespace='video')),
    re_path(r'^tcmquery/', include(('apps.tcm_query.urls', 'apps.tcm_query'), namespace='tcm_query')),
    path(r'', include(('apps.tcm_query.urls', 'apps.tcm_query'), namespace='tcm_query_1')),

              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
