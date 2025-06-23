# dashboard/forms.py
from django import forms
from .models import Result, Semester, Session
from django.contrib.auth import get_user_model

User = get_user_model()

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'course_of_study', 'session', 'semester', 'results_detail']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course_of_study': forms.Select(attrs={'class': 'form-control mb-3'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'results_detail': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)

        # Apply the CSS class to all fields
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()
            
            # Add placeholder-like label to student select
        self.fields['student'].empty_label = "-- Select Your Student --"

        if teacher and teacher.profile.faculty:
            self.fields['student'].queryset = User.objects.filter(
                user_type='student',
                profile__faculty=teacher.profile.faculty
            )
        else:
            self.fields['student'].queryset = User.objects.none()

class CheckResult(forms.Form):
    session = forms.ModelChoiceField(
    queryset=Session.objects.all(),
    empty_label="Select a session",
    required=True,
    widget=forms.Select(attrs={'class': 'form-select'})
)

    semester = forms.ModelChoiceField(
    queryset=Semester.objects.all(), 
    empty_label="Select a Semester",
    required=True,  
    widget=forms.Select(attrs={'class': 'form-select'}))
