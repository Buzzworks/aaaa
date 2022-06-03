"""flexydial URL Configuration

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
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from . import views
from callcenter import views as callcenter
from crm import views as crm
from django.conf import settings
#import debug_toolbar
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path(r'', include('callcenter.urls')),
    path(r'',include('crm.urls')),
    path(r'', callcenter.LoginAPIView.as_view(), name='login'),
    path(r'dashboard/',callcenter.DashBoardApiView.as_view(), name="dashboard" ),
    path(r'get_latest_notification/',callcenter.GetLatestNoificationView.as_view(),
        name="get-latest-notification" ),

    path(r'change_password/',views.ChangePasswordApiView.as_view(), name="change_password"),
    path(r'logout/', callcenter.LogoutAPIView.as_view(), name='logout'),
    path(r'logout/<str:makeInactive>/', callcenter.LogoutAPIView.as_view(), name='logout'),
    path('api/delete-selected-entry/',
         views.DeleteEntryApiView.as_view(), name="delete-entries"),
    path('api/check-selected-entry/',
         views.CheckCanEditView.as_view(), name="check_can_edit"),
    path('api/fetch-existing-data/',
         views.FetchExistingDataApiView.as_view(), name="fetch-existing-data"),
    path('api/download-sample-file/<str:file_name>/<str:file_type>/',
         views.DownloadSampleApiView.as_view(), name="download-sample-file"),
    path('api/download-sample-contact-file/<str:col_name>/<str:file_type>/',
         views.DownloadSampleContactApiView.as_view(), name="download-sample-contact-file"),
    path('api/charts/',TemplateView.as_view(template_name= 'reports/charts.html'),name='charts'),
    path('api/system-boot-action/', views.SystemBootAction.as_view(), name='system-boot-action'),

    path("password-reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset-confirm/<uidb64>/<token>", views.CustomPasswordResetConfirmView.as_view( template_name="registration/password_reset_confirm.html",form_class=views.CustomPasswordResetForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete")

] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

