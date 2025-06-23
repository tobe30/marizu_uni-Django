from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.Registerview, name="sign-up"),
    path("sign-in/", views.Loginview, name="sign-in"),
    path("logout/", views.logoutView, name="logout"),

    
]