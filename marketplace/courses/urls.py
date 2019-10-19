from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_courses', views.add_courses, name='add_courses'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('add_entry/<int:pk>/', views.add_entry, name='add_entry'),
    path('save_lesson/<int:pk>/', views.save_lesson, name='save_lesson'),
    path('lesson/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('save_video/<int:pk>/', views.save_video, name='save_video'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('enroll/<int:pk>/', views.course_enroll, name='course_enroll'),
]
