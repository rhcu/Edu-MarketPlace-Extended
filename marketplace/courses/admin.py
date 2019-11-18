from django.contrib import admin
from .models import Course, UserAnswer, UserQuizPassed

admin.site.register(Course)
admin.site.register(UserAnswer)
admin.site.register(UserQuizPassed)
