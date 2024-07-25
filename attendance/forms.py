from django import forms
from .models import Course, Subject

class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = [
			"name",
		]


class SubjectForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = [
			"name",
			"present",
			"absent",
		]