from django import forms


class CourseSearchForm(forms.Form):
    query = forms.CharField(
        label="Custom query",
        required=False,
    )
    title = forms.CharField(
        label="Title",
        required=False,
    )
    description = forms.CharField(
        label="Description",
        required=False,
    )
    topic = forms.CharField(
        label="Topic",
        required=False,
    )
