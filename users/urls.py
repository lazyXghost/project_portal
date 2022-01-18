from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls.conf import include
from . import views


urlpatterns = [
    path('<int:user_id>/cv', views.profile_cv_view, name = 'profile_cv_view'),
    path('<int:user_id>', views.profile, name = 'profile'),
    path('edit/', views.profile_edit, name = 'profile-edit'),
    path('projects/view/', views.projects_view, name = 'projects-view'),
]
