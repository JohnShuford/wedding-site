"""
URL configuration for wedding_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Redirect root URL to Home
def redirect_to_rsvp(request):
     return redirect('/wedding/')

urlpatterns = [
    path('', redirect_to_rsvp, name='home_redirect'),
    path('admin/', admin.site.urls),
    # path('rsvp/', include('rsvp.urls')),
    # Keep wedding pages accessible under /wedding/ path
    path('wedding/', include('wedding.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)