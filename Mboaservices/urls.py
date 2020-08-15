"""Mboaservices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import (
	path, include)
from django.conf.urls.static import static
from django.shortcuts import render

from . import settings


def render_home_page(request, id=None):
    return render(request, 'build/index.html')


urlpatterns = [
    path('', render_home_page),
    path('admin/', admin.site.urls),
    path('client/', include('Client.urls')),
    path('dish/', include('Dishes.urls')),
    path('invigilator/', include('Invigilator.urls')),
    path('orders/', include('Orders.urls')),
    path('restaurant/', include('Restaurant.urls')),
    path('reviews/', include('Reviews.urls')),
    path('user/', include('User.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Mboaservices Admin Panel'
admin.site.site_title = 'Mboaservices'