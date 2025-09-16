from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['label', 'std_id', 'name', 'gender','dob', 'tel', 'batch','major']