from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CourseForm
from django.shortcuts import redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Course

def index(request):
    userdata = {}
    user = request.user
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
        'userdata': userdata
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
    return render(request, 'add_courses.html', {'form':form})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'course_detail.html', {'course': course})
