from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('profile', views.profile),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
]
