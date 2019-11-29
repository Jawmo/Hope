from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from . import views

# from .views import play, sign_up, login_page, display_news


urlpatterns = [
    path('', views.index, name='index'),
    path(r'accounts/login/', views.login_page, name='login_page'),
    path(r'signup/', views.sign_up, name='sign_up'),
    path(r'play/', views.play, name='play'),
    # path(r'^home/$', display_news, name='home'),

    path(r'admin/', admin.site.urls),
]