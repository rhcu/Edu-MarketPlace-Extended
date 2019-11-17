from django.db import models
from django.conf import settings
from decimal import Decimal


class Course(models.Model):
    # Information about the course
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    topic = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    date_created = models.DateTimeField('date published')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.0000'))
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.title


ENTRIES_CHOICES = (
    ('lesson', 'Lesson'),
    ('video', 'Video'),
    ('quiz', 'Quiz'),
)


class CourseEntry(models.Model):
    # Meta data about course entry, full data stored within course
    # entry types
    name = models.CharField(max_length=500)
    entry_type = models.CharField(max_length=100, choices=ENTRIES_CHOICES, default='lesson')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,)
    date_created = models.DateTimeField('date published')

    def __str__(self):
        return self.name + " in " + self.course.title


class Lesson(models.Model):
    # Lesson (rich text) type of course entry
    course_entry = models.ForeignKey(CourseEntry, on_delete=models.CASCADE,)
    content = models.TextField()


class Video(models.Model):
    # Video type of course entry
    course_entry = models.ForeignKey(CourseEntry, on_delete=models.CASCADE,)
    video_url = models.URLField(max_length=1000)


class CourseEnroll(models.Model):
    # User enrollment storage
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " enrolled in " + self.course.title + ", course_id=" + str(self.course_id)


class Quiz(models.Model):
    # Quiz type of course entry
    course_entry = models.ForeignKey(CourseEntry, on_delete=models.CASCADE,)


class Question(models.Model):
    # Many questions per one quiz
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,)
    name = models.CharField(max_length=200)


class Answer(models.Model):
    # Many possible answers per one question
    question = models.ForeignKey(Question, on_delete=models.CASCADE,)
    name = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)


class CourseProgression(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_entry = models.ForeignKey(
        CourseEntry, on_delete=models.CASCADE, limit_choices_to={'course': course})
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "CourseProgression: user=" + self.user.username + " course='" + self.course.title + \
               "', course_entity='" + self.course_entry.name + ", completed=%r" % self.completed