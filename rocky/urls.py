"""rocky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf import settings
from django.conf.urls import include, static, url
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    # Handle favicon at root
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('favicon.ico')
    ), name='favicon'),
    # Django included
    path('admin/', admin.site.urls),
    path('user/', include('django.contrib.auth.urls')),
    # Installed apps
    url('notifications/', include('notify.urls', 'notifications')),
    url('tinymce/', include('tinymce.urls')),
    # Site apps
    url('', include('landingpage.urls')),
    url('cast/', include('castpage.urls')),
    url('cast/admin/', include('castadmin.urls')),
    url('user/', include('useradmin.urls')),
    url('profile/', include('userprofile.urls')),
    url('event/', include('events.urls')),
    url('search/', include('search.urls')),
]

# If running locally:
if settings.MEDIA_URL:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
