from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, CourseEntryForm, LessonSaveForm, VideoSaveForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Course, CourseEntry, Lesson, Video, CourseEnroll, Quiz, Question, Answer
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db.models import Q


def is_course_owner(course, user):
    return course.owner == user


def is_user_enrolled(course, user):
    if not user or not user.is_authenticated:
        return False
    if course.owner == user:
        return True
    enroll_count = CourseEnroll.objects.filter(course=course, user=user).count()
    return enroll_count > 0


def get_lesson(course_entry_pk):
    course_entry = get_object_or_404(CourseEntry, pk=course_entry_pk)
    return Lesson.objects.filter(course_entry=course_entry)[0]


def get_video(course_entry_pk):
    course_entry = get_object_or_404(CourseEntry, pk=course_entry_pk)
    return Video.objects.filter(course_entry=course_entry)[0]


def get_quiz(course_entry_pk):
    course_entry = get_object_or_404(CourseEntry, pk=course_entry_pk)
    return Quiz.objects.filter(course_entry=course_entry)[0]


def index(request):
    userdata = {}
    user = request.user
    if user.is_authenticated:
        course_objects = Course.objects.filter(Q(visible=True) | Q(owner=user))
    else:
        course_objects = Course.objects.filter(Q(visible=True))
    courses = []
    if user.is_authenticated:
        user = request.user
        auth0user = user.social_auth.get(provider='auth0')
        userdata = {
            'user_id': auth0user.uid,
            'name': user.first_name,
            'picture': auth0user.extra_data['picture'],
            'email': auth0user.extra_data['email'],
        }
    for course in course_objects:
        courses.append(
            (course, (is_user_enrolled(course, user), is_course_owner(course, user))))
    return render(request, 'courses.html', {
        'userdata': userdata,
        'courses': courses,
    })


@login_required
def add_courses(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.date_created = timezone.now()
            course.save()
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'add_courses.html', {'form': form})


@login_required
def save_lesson(request, pk):
    user = None
    if request.user.is_authenticated:
        user = request.user
    lesson = get_object_or_404(Lesson, pk=pk)
    course_entry = lesson.course_entry
    course = course_entry.course
    if user == course.owner:
        form = LessonSaveForm()
        form.fields['content'].initial = lesson.content
        if request.method == 'POST':
            form = LessonSaveForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                lesson.content = cd.get('content', '')
                lesson.save()
                return redirect('lesson_detail', pk=course_entry.pk)
        return render(request, 'save_lesson.html', {'lesson': lesson, 'user': user, 'form': form})
    return redirect('course_detail', pk=course.pk)


@login_required
def lesson_detail(request, pk):
    # pk - primary key for course entry and NOT LESSON
    if request.user.is_authenticated:
        user = request.user
        lesson = get_lesson(pk)
        if is_user_enrolled(lesson.course_entry.course, user):
            return render(request, 'lesson_detail.html', {'lesson': lesson, 'user': user})
    return redirect('course_detail', pk=lesson.course_entry.course.pk)


@login_required
def save_video(request, pk):
    user = None
    if request.user.is_authenticated:
        user = request.user
    video = get_object_or_404(Video, pk=pk)
    course_entry = video.course_entry
    course = course_entry.course
    if user == course.owner:
        form = VideoSaveForm()
        form.fields['video_url'].initial = video.video_url
        if request.method == "POST":
            form = VideoSaveForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                video.video_url = cd.get("video_url", "")
                video.save()
                return redirect('video_detail', pk=course_entry.pk)
        return render(request, 'save_video.html', {'video': video, 'user': user, 'form': form})
    return redirect('course_detail', pk=course.pk)


@login_required
def video_detail(request, pk):
    # pk - primary key for course entry and NOT VIDEO
    if request.user.is_authenticated:
        user = request.user
        video = get_video(pk)
        if is_user_enrolled(video.course_entry.course, user):
            return render(request, 'video_detail.html', {'video': video, 'user': user})
    return redirect('course_detail', pk=video.course_entry.course.pk)


@login_required
def save_question(request, quiz_pk):
    if request.user.is_authenticated:
        user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    course_entry = quiz.course_entry
    course = course_entry.course
    if user == course.owner:
        if request.method == 'POST':
            name = request.POST.get('name', '')
            pk = request.POST.get('pk', None)
            if pk:
                # Change question name, if it already exists
                question = get_object_or_404(Question, pk=pk)
            else:
                question = Question()
            question.name = name
            question.quiz = quiz
            question.save()
            obj = serializers.serialize('json', [question])
            return HttpResponse(obj, content_type="text/json-comment-filtered")
    return redirect('course_detail', pk=course.pk)


@login_required
def save_answer(request, question_pk):
    if request.user.is_authenticated:
        user = request.user
    question = get_object_or_404(Question, pk=question_pk)
    quiz = get_object_or_404(Quiz, pk=question.quiz.pk)
    course_entry = quiz.course_entry
    course = course_entry.course
    if user == course.owner:
        if request.method == 'POST':
            name = request.POST.get('name', '')
            correct = 'true' in request.POST.get('correct')
            pk = request.POST.get('pk', None)
            if pk:
                # Change answer name, if it already exists
                answer = get_object_or_404(Answer, pk=pk)
            else:
                answer = Answer()
            answer.name = name
            answer.correct = correct
            answer.question = question
            answer.save()
            obj = serializers.serialize('json', [answer])
            return HttpResponse(obj, content_type="text/json-comment-filtered")
    return redirect('course_detail', pk=course.pk)


@login_required
def quiz_detail(request, pk):
    # pk - primary key for course entry and NOT LESSON
    if request.user.is_authenticated:
        user = request.user
        quiz = get_quiz(pk)
        if is_user_enrolled(quiz.course_entry.course, user):
            return render(request, 'quiz_detail.html', {'quiz': quiz, 'user': user})
    return redirect('course_detail', pk=quiz.course_entry.course.pk)


@login_required
def get_quiz_content(request, quiz_pk):
    if request.user.is_authenticated:
        user = request.user
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    course_entry = quiz.course_entry
    course = course_entry.course
    if user == course.owner or is_user_enrolled(course, user):
        if request.method == 'GET':
            questions = Question.objects.filter(quiz=quiz)
            arr_questions = []
            for question in questions:
                answers = Answer.objects.filter(question=question)
                arr_answers = []
                for answer in answers:
                    if user == course.owner:
                        dict_answer = {'name': answer.name, 'correct': answer.correct}
                    else:
                        dict_answer = {'name': answer.name}
                    arr_answers.append(dict_answer)
                dict_question = {'answers': arr_answers, 'name': question.name, 'pk': question.pk}
                arr_questions.append(dict_question)
            return JsonResponse({'questions': arr_questions})
    return redirect('course_detail', pk=course.pk)



@login_required
def save_quiz(request, pk):
    user = None
    if request.user.is_authenticated:
        user = request.user
    quiz = get_object_or_404(Quiz, pk=pk)
    course_entry = quiz.course_entry
    course = course_entry.course
    if user == course.owner:
        return render(request, 'save_quiz.html', {'quiz': quiz, 'user': user})
    return redirect('course_detail', pk=course.pk)


@login_required
def add_entry(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    if user == course.owner:
        if request.method == 'POST':
            form = CourseEntryForm(request.POST)
            if form.is_valid():
                course_entry = form.save(commit=False)
                course_entry.date_created = timezone.now()
                course_entry.course = course
                course_entry.save()
                if course_entry.entry_type == 'lesson':
                    lesson = Lesson()
                    lesson.course_entry = course_entry
                    lesson.content = 'Here will be the content of your course!'
                    lesson.save()
                    return redirect('save_lesson', pk=lesson.pk)
                elif course_entry.entry_type == 'video':
                    video = Video()
                    video.course_entry = course_entry
                    video.save()
                    return redirect('save_video', pk=video.pk)
                elif course_entry.entry_type == 'quiz':
                    quiz = Quiz()
                    quiz.course_entry = course_entry
                    quiz.save()
                    return redirect('save_quiz', pk=quiz.pk)
                else:
                    raise Exception('Course entry is not found')
        else:
            form = CourseEntryForm()
        return render(request, 'add_entry.html', {'course': course, 'user': user, 'form': form})
    else:
        return redirect('course_detail', pk=course.pk)


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    course_entries = CourseEntry.objects.filter(course=course)
    user = None
    if request.user.is_authenticated:
        user = request.user
    user_enrolled = is_user_enrolled(course, user)
    return render(request, 'course_detail.html',
                  {'course': course, 'user': user, 'course_entries': course_entries, 'user_enrolled': user_enrolled})


@login_required
def course_enroll(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        enroll = CourseEnroll()
        enroll.user = user
        enroll.course = course
        enroll.save()
    # In any case, just redirect to course detail
    return redirect('course_detail', pk=course.pk)


@login_required
def course_unenroll(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    CourseEnroll.objects.filter(user=user, course=course).delete()
    return redirect('course_detail', pk=course.pk)


@login_required
def enrolled_list(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    if user == course.owner:
        enrolled_objects = CourseEnroll.objects.filter(course=course)
        users = [obj.user for obj in enrolled_objects]
        return render(request, 'enrolled_list.html', {'enrolled_users': users, 'user': user, 'course': course})
    else:
        return redirect('course_detail', pk=course.pk)


def get_user_detail(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user,
        'courses': Course.objects.filter(owner=user)
    }
    return render(request, 'user_courses.html', context)
