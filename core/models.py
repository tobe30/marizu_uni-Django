from django.db import models
from shortuuid.django_fields import ShortUUIDField
from dashboard.models import Faculty
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from userauths.models import Profile
from django.dispatch import receiver
from django.utils.crypto import get_random_string
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

CHOICES=[
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

# Create your models here.
def user_directory_path(instance, filename):
    return f"applications/{filename}"

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return self.name



class Application(models.Model):
    aid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="aid123" )
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    jamb_reg_number = models.CharField(max_length=50)
    jamb_score = models.PositiveIntegerField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name="course")
    jamb_document = models.FileField(upload_to=user_directory_path, default='default.pdf')
    waec_document = models.FileField(upload_to=user_directory_path, default='default.pdf')
    date_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOICES, default='Pending')
    
    def __str__(self):
        return self.full_name
    
    
    

@receiver(post_save, sender=Application)
def create_student_account(sender, instance, created, **kwargs):
    if instance.status == 'Accepted':
        user = User.objects.filter(email=instance.email).first()
        
        if not user:
            password = get_random_string(length=10)
            user = User.objects.create_user(
                email=instance.email,
                username=instance.full_name.replace(" ", ""),
                user_type='student',
                password=password
            )
        else:
            password = None  # Already exists

        # Now, update or create the profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.full_name = instance.full_name
        profile.phone = instance.phone
        profile.faculty = instance.course.faculty if instance.course else None
        profile.save()

        if password:
            print(f"Generated password for {user.email} is: {password}")

            # logger.info(f"Generated for {user.email} is: {password}") 
            # cindy k1Iw0k4alm
            # divine ghby9MDkav
            # camsy 1QIgGLgIxG
            