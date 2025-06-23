from django.contrib import admin
from core.models import Course, Application

# Register your models here.

class AppAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'jamb_reg_number', 'jamb_score', 'course', 'status')
    
admin.site.register(Application, AppAdmin)
admin.site.register(Course)