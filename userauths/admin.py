from django.contrib import admin
from userauths.models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'user_type')

admin.site.register(User, UserAdmin)
admin.site.register(Profile)

# Register your models here.