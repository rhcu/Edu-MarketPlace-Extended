from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from elasticsearch import TransportError
from elasticsearch_dsl.query import Q
from .documents import CourseDocument
from .helper import SearchResults


def search(request):
    paginate_by = 20
    courses_search = CourseDocument.search()
    query = request.GET.get('query')

    if query:
        courses_search = courses_search.query(
            Q('match', title=query) |
            Q('match', topic=query) |
            Q('match', description=query)
        )

    search_results = SearchResults(courses_search)

    paginator = Paginator(search_results, paginate_by)
    page_number = request.GET.get("page")
    try:
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # If page parameter is not an integer, show first page.
            page = paginator.page(1)
        except EmptyPage:
            # If page parameter is out of range, show last existing page.
            page = paginator.page(paginator.num_pages)
    except TransportError:
        raise Http404('Index does not exist.')

    context = {
        'object_list': page,
    }
    return render(request, 'search.html', context)
