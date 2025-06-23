from django.shortcuts import render, redirect
from .forms import AppForm
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, "core/index.html")

def application(request):
    if request.method == "POST":
        form = AppForm(request.POST, request.FILES)  # Ensure FILES is included if you're handling file uploads
        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Application submitted successfully and is under review.")
                return redirect("core:application")
            else:
                # Show form validation errors using Django messages
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = AppForm()

    return render(request, "core/application.html", {"form": form})