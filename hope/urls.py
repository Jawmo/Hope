from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from accounts import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]