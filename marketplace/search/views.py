from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from elasticsearch import TransportError
from elasticsearch_dsl.query import Q
from .documents import CourseDocument, UserDocument
from .helper import SearchResults
from .forms import SearchForm


def search(request):
    form = SearchForm(data=request.GET)
    context = {
        'object_list': None,
        'form': form,
        'category': None
    }

    if form.is_valid():
        query = form.cleaned_data['query']
        category = form.cleaned_data['category']

        if query and category:
            paginate_by = 20
            search_results = None

            if category == 'courses':
                courses_search = CourseDocument.search()
                search_results = courses_search.query(
                    Q('match', title=query) |
                    Q('match', topic=query) |
                    Q('match', description=query)
                )

            elif category == 'users':
                users_search = UserDocument.search()
                search_results = users_search.query(
                    Q('match', username=query) |
                    Q('match', first_name=query) |
                    Q('match', last_name=query) |
                    Q('match', email=query)
                )

            search_results = SearchResults(search_results)

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
                'form': form,
                'category': category
            }
    return render(request, 'search.html', context)
