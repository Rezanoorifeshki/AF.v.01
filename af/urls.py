"""
URL configuration for af project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from afapp.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('shop/', shop),
    path('shopcat/<add>', shopcat),
    path('shopproduct/<add>', shopproduct),
    path('contactus/', contactus),
    path('thanks/', thanks),
    path('aboutus/', aboutus),
    path('login/', login),
    path('account/',account),



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
