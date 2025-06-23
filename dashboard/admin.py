from django.contrib import admin
from dashboard.models import Faculty, Result, Semester, Session, AcceptancePayment, SchoolFeePayment, HostelPayment

# Register your models here.


class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_of_study', 'session', 'semester', 'added_by')

admin.site.register(Faculty)
admin.site.register(Semester)
admin.site.register(Session)
admin.site.register(Result, ResultAdmin)
admin.site.register(AcceptancePayment)
admin.site.register(SchoolFeePayment)
admin.site.register(HostelPayment)
