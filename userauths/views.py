from django.shortcuts import render, redirect
from django.contrib import messages
from userauths.forms import UserRegistrationForm
from django.contrib.auth import login, logout
from userauths.models import User
from django.contrib.auth import authenticate



# Create your views here.


def Registerview(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Access Denied..")
        
        return redirect('core:index')
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your account was created successfully")
            login(request, new_user)
            return redirect("core:index")
        else:
            messages.error(request, "There was an error in the form. Please correct it.")
    
    else:
        form = UserRegistrationForm()
    context ={
        "form":form,
    }
    return render(request, "userauths/register.html", context)

def Loginview(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request,email=email, password=password)
            
            if user is not None:
                login(request, user)
                user_type = user.user_type
                if user_type == 'student':
                    messages.success(request, "You are logged in")
                    return redirect("dashboard:stu_dashboard")
                elif user_type == 'teacher':
                    messages.success(request, "You are logged in")
                    return redirect("dashboard:dashboard")
            else:
                messages.warning(request, "email or password does not exist")
                return redirect("userauths:sign-in")
        except:
            messages.warning(request, f"User with this{email} does not exist")
            
    if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect("core:index")
    return render(request, "userauths/login.html")


def logoutView(request):
      logout(request)
      messages.success(request, "You have been logged out")
      return redirect("userauths:sign-in")