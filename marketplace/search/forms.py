from django import forms
from django.utils.translation import ugettext_lazy as _


class SearchForm(forms.Form):
    CHOICES = [('users', 'Users'),
               ('courses', 'Courses')]

    query = forms.CharField(
        label=_("Your search query"),
        required=False,
    )
    category = forms.ChoiceField(
        choices=CHOICES,
        label=_("Search by"),
        required=False,
    )
