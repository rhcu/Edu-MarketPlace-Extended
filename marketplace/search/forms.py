from django import forms
from django.utils.translation import ugettext_lazy as _


class CourseSearchForm(forms.Form):
    query = forms.CharField(
        label=_("Custom query"),
        required=False,
    )
    title = forms.CharField(
        label=_("Title"),
        required=False,
    )
    description = forms.CharField(
        label=_("Description"),
        required=False,
    )
    topic = forms.CharField(
        label=_("Topic"),
        required=False,
    )
