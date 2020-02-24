from django import forms
from django.utils.functional import LazyObject


class SearchResults(LazyObject):
    def _setup(self):
        pass

    def __init__(self, search_object):
        super().__init__()
        self._wrapped = search_object

    def __len__(self):
        return self._wrapped.count()

    def __getitem__(self, index):
        search_results = self._wrapped[index]
        if isinstance(index, slice):
            search_results = list(search_results)
        return search_results
