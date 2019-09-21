from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_courses', views.add_courses, name='add_courses')
]
