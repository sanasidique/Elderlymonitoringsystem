"""
URL configuration for monitoringsystem project.

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
from django.urls import path,include
from . import views
urlpatterns = [

    path('main/', views.main),
    path('login_get/', views.login_get),
    path('logout/', views.logout),
    path('home/', views.home),
    path('add_caretaker/', views.add_caretaker),
    path('assign_caretaker/', views.assign_caretaker),
    path('edit_caretaker/<id>', views.edit_caretaker),
    path('send_reply/<id>', views.send_reply),
    path('send_reply_post/', views.send_reply_post),
    path('view_complaint_send_reply/', views.view_complaint_send_reply),
    path('view_request_assigned/', views.view_request_assigned),
    path('add_caretaker_post/', views.add_caretaker_post),
    path('edit_caretaker_post/', views.edit_caretaker_post),
    path('upload/', views.upload),
    path('delete_caretaker/<id>', views.delete_caretaker),

    path('loginpost/', views.loginpost),
    path('view_aasigned_user/', views.view_aasigned_user),
    path('pill_reminder/', views.pill_reminder),
    path('user_view_caretaker/', views.user_view_caretaker),
    path('user_view_assigned_caretaker/', views.user_view_assigned_caretaker),
    path('add_patient/', views.add_patient),
    path('delete_patient/', views.delete_patient),
    path('edit_patient/', views.edit_patient),
    path('caretaker_view_profile/', views.caretaker_view_profile),
    path('user_view_patients/', views.user_view_patients),
    path('user_view_pill_notifications/', views.user_view_pill_notifications),
    path('user_view_patients/', views.user_view_patients),
    path('registration/', views.registration),
    path('view_profile/', views.view_profile),
    path('update_profile/', views.update_profile),
    path('send_complaint/', views.send_complaint),
    path('view_complaint/', views.view_complaint),
    path('send_caretaker_request/', views.send_caretaker_request),
    path('view_request_for_caretaker/', views.view_request_for_caretaker),
    path('user_view_request/', views.user_view_request),
    path('caretaker_view_assigned/', views.caretaker_view_assigned),
    path('caretaker_add_pill/', views.caretaker_add_pill),
    path('caretaker_view_pills/', views.caretaker_view_pills),
    path('assign_caretaker/<id>', views.assign_caretaker),
    path('get_fall_notifications/', views.get_fall_notifications),
    path('get_notifications/', views.get_notifications_emergency),
    path('get_pill_reminder/', views.get_pill_reminder),
# urls.py
path('get_fall_notifications/', views.get_fall_notifications, name='get_fall_notifications'),
]
