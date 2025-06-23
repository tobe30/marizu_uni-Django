from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Profile
from dashboard.models import Faculty


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control'
    }))
    email = forms.EmailField( widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email Address',
            'class': 'form-control'
        }))
    password1 = forms.CharField( widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter Your Password',
            'class': 'form-control'
        }))
    password2 = forms.CharField( widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Your Password',
            'class': 'form-control'
        }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    


####### Profile Edit ##########
class ProfileForm(forms.ModelForm):
   email = forms.EmailField(disabled=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))
   username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

   full_name = forms.CharField(disabled=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Full Name',
        "class":"form-control"
    }))
    
   phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Phone Number',
        "class":"form-control"
    }))
   level = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control",
        'readonly':'readonly'
        
    }))
    
   bio = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Bio',
        "class":"form-control"
    }))
   faculty = forms.ModelChoiceField(
    queryset=Faculty.objects.all(),
    required=True,  # This goes here
    widget=forms.Select(attrs={
        'class': 'form-control form-select',
    })
)

   
    
    
   class Meta:
        model = Profile
        fields = ['full_name', 'email', 'bio', 'phone', 'faculty', 'level']
        
   def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username