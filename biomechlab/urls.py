"""biomechlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from biomechlabwebapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.conf.urls import url
from django.contrib.auth import views as auth_views 
from django.urls import path, include


app_name = 'biomechlabwebapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('uploadFile/', views.uploadFile, name='uploadFile'),
    path('retrieveData/', views.retrieveData,name='retrieveData'),
    path('getAllData/', views.getAllData,name='getAllData'),
    path('accounts', include('django.contrib.auth.urls')),
    path('home', TemplateView.as_view(template_name='home.html'), name='home'),
    path('retrieveDataEnglish', views.retrieveDataEnglish,name='retrieveDataEnglish'),
    path('uploadFileEnglish', views.uploadFileEnglish,name='uploadFileEnglish'),
    path('blandAltman/', views.uploadDataset,name='blandAltman'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    url(r'^delete/(?P<id>[0-9]+)/$', views.deleteData, name='deleteData'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)