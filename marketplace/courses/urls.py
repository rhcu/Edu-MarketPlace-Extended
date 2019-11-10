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
    path('unenroll/<int:pk>/', views.course_unenroll, name='course_unenroll'),
    path('enrolled_list/<int:pk>/', views.enrolled_list, name='enrolled_list'),
    path('user_courses/<str:username>', views.get_user_detail, name='user_detail'),
    path('save_quiz/<int:pk>/', views.save_quiz, name='save_quiz'),
    path('save_question/<int:quiz_pk>/', views.save_question, name='save_question'),
    path('save_answer/<int:question_pk>/', views.save_answer, name='save_answer'),
    path('get_quiz_content/<int:quiz_pk>/', views.get_quiz_content, name='get_quiz_content'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
]
