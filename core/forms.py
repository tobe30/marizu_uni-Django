from django import forms
from core.models import Application, Course


class AppForm(forms.ModelForm):
    
    
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Full Name',
        "class":"form-control"
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Your Email Address',
        "class":"form-control"
    }))
    
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Phone Number',
        "class":"form-control"
    }))
    
    jamb_reg_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your JAMB Registration Number',
        "class":"form-control"
    }))
    
    jamb_score = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Your JAMB Score',
        "class":"form-control"
    }))

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),  # Fetch all categories from the database
        widget=forms.Select(attrs={
            'class': 'form-control form-select',
            'required': 'required',
        }),
        empty_label="Select course",  # This will be the first option in the dropdown
    )
    
    jamb_document = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'id': 'document-input',
        'accept': '.pdf,.jpg,.jpeg,.png',
        'hidden':True
    }))
    
    waec_document = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'id': 'waec-document-input',
        'accept': '.pdf,.jpg,.jpeg,.png',
        'hidden':True
    }))
    
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'phone', 'jamb_reg_number', 'jamb_score', 'course', 'jamb_document', 'waec_document']
    