from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse


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
    return render(request, 'add_courses.html', {})
