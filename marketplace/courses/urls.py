from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_courses', views.add_courses, name='add_courses'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('certificate/<int:pk>/', views.course_certificate, name='course_certificate'),
    path('pay/<int:pk>/', views.course_pay, name='course_pay'),
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
    path('add_user_answer/<int:answer_pk>/', views.add_user_answer, name='add_user_answer'),
    path('get_user_answer/<int:answer_pk>/', views.get_user_answer, name='get_user_answer'),
    # If submitted with POST method, will add current user to those who passed quiz
    path('user_passed_quiz/<int:quiz_pk>/', views.user_passed_quiz, name='user_passed_quiz'),
    path('get_quiz_content/<int:quiz_pk>/', views.get_quiz_content, name='get_quiz_content'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('get_progress/<int:course_pk>', views.get_progress, name='progress'),
    path('delete_lesson/<int:pk>', views.delete_lesson, name='delete_lesson'),
    path('delete_video/<int:pk>', views.delete_video, name='delete_video'),
    path('mark_lesson/<int:pk>', views.mark_lesson, name='mark_lesson'),
    path('mark_video/<int:pk>', views.mark_video, name='mark_video'),
    path('get_course_rating/<int:course_pk>', views.get_course_rating, name='get_course_rating'),
    path('get_user_rating/<int:course_pk>', views.get_user_rating, name='get_user_rating'),
    re_path(r'^set_rating/(?P<course_pk>[0-9]+)/(?P<rating>[0-9]+)/$', views.set_course_rating,
            name='set_course_rating')
]

