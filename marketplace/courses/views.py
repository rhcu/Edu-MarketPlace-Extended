from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, CourseEntryForm, LessonSaveForm, VideoSaveForm
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Course, CourseEntry, Lesson, Video

def user_enrolled(course, user):
    if user == False:
        return False
    if course.owner == user:
        return True
    # TODO: https://github.com/rhcu/Edu-MarketPlace-Extended/issues/32
    return True

def index(request):
    userdata = {}
    user = request.user
    courses = Course.objects.all()
    if user.is_authenticated:
        user = request.user
        auth0user = user.social_auth.get(provider='auth0')
        userdata = {
            'user_id': auth0user.uid,
            'name': user.first_name,
            'picture': auth0user.extra_data['picture'],
            'email': auth0user.extra_data['email'],
        }
    return render(request, 'courses.html', {
        'userdata': userdata,
        'courses': courses
    })


@login_required
def add_courses(request):
    if request.method == "POST":
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
        if request.method == "POST":
            form = LessonSaveForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                lesson.content = cd.get("content", "")
                lesson.save()
                return redirect('lesson_detail', pk=lesson.pk)
        return render(request, 'save_lesson.html', {'lesson': lesson, 'user': user, 'form': form})
    return redirect('course_detail', pk=course.pk)

@login_required
def lesson_detail(request, pk):
    user = None
    if request.user.is_authenticated:
        user = request.user
        lesson = get_object_or_404(Lesson, pk=pk)
        if user_enrolled(lesson.course_entry.course, user):
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
                return redirect('video_detail', pk=video.pk)
        return render(request, 'save_video.html', {'video': video, 'user': user, 'form': form})
    return redirect('course_detail', pk=course.pk)


@login_required
def video_detail(request, pk):
    user = None
    if request.user.is_authenticated:
        user = request.user
        video = get_object_or_404(Video, pk=pk)
        if user_enrolled(video.course_entry.course, user):
            return render(request, 'video_detail.html', {'video': video, 'user': user})
    return redirect('course_detail', pk=video.course_entry.course.pk)


@login_required
def add_entry(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)
    if user == course.owner:
        if request.method == "POST":
            form = CourseEntryForm(request.POST)
            if form.is_valid():
                course_entry = form.save(commit=False)
                course_entry.date_created = timezone.now()
                course_entry.course = course
                course_entry.save()
                if course_entry.entry_type == 'lesson':
                    lesson = Lesson()
                    lesson.course_entry = course_entry
                    lesson.content = "Here will be the content of your course!"
                    lesson.save()
                    return redirect('save_lesson', pk=lesson.pk)
                elif course_entry.entry_type == 'video':
                    video = Video()
                    video.course_entry = course_entry
                    video.save()
                    return redirect('save_video', pk = video.pk)
                else:
                    raise Exception("Course entry is not found")
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
    return render(request, 'course_detail.html', {'course': course, 'user': user, 'course_entries': course_entries})
