from django import forms

from .models import Course, CourseEntry

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('title', 'description', 'topic', 'price')


class CourseEntryForm(forms.ModelForm):
	class Meta:
		model = CourseEntry
		fields = ('name', 'entry_type',)


class LessonSaveForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea)


class VideoSaveForm(forms.Form):
	video_url = forms.URLField(label='Link to YouTube video', required=True)

