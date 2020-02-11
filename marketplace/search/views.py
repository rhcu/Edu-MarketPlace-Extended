from django.shortcuts import render
from search.documents import CourseDocument


def search(request):
    query = request.GET.get('query')

    if query:
        courses = CourseDocument.search().query("match", title=query)
        if courses.count() == 0:
            courses = None
    else:
        courses = None

    return render(request, 'search.html', {'courses': courses})
