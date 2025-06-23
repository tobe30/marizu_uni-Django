from django.db import models
from django.conf import settings


# Create your models here.
# in your models.py
class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(max_length=100)  # e.g., "2024/2025"
    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=20)  # e.g., "First", "Second"
    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='results')
    course_of_study = models.ForeignKey('core.Course', on_delete=models.CASCADE, related_name='results')
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    results_detail = models.TextField(
        help_text="Enter results as plain text, e.g.\nmath - A\ncsc101 - A\nphy - C"
    )
    
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='added_results')  # The teacher

    def __str__(self):
        return f"Result of {self.student} for {self.session} {self.semester}"
    
    
class AcceptancePayment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(auto_now_add=True)
    tx_ref = models.CharField(max_length=100, unique=True, default='123')

    def __str__(self):
        return f"Acceptance - {self.student} - {self.session}"
    
class HostelPayment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(auto_now_add=True)
    tx_ref = models.CharField(max_length=100, unique=True, default='123')
    
    


class SchoolFeePayment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(auto_now_add=True)
    tx_ref = models.CharField(max_length=100, unique=True, default='123')

    def __str__(self):
        return f"School Fees - {self.student} - {self.session} {self.semester}"



