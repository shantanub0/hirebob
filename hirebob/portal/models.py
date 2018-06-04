from django.db import models
from django.conf import settings

BASE_DIR = settings.BASE_DIR


# Create your models here.
def user_directory_path(instance, filename):
    return "portal/static/profile_images/{0}/{1}".format(instance.email, filename)


def user_dir_path(instance, filename):
    return "portal/static/resumes/{0}/{1}".format(instance.email, filename)


class UserType(models.Model):
    user_type_name = models.TextField(max_length=20)


class UserAccount(models.Model):
    user_acc_id = models.AutoField(primary_key=True)
    user_type = models.TextField(max_length=20)
    user_full_name = models.TextField(max_length=100)
    email = models.EmailField()
    password = models.TextField(max_length=50)
    date_of_birth = models.DateField(default=None, null=True)
    gender = models.TextField(max_length=1)
    is_active = models.TextField(max_length=1)
    contact_number = models.IntegerField(default=None, null=True)
    sms_notification_active = models.TextField(max_length=1)
    email_notification_active = models.TextField(max_length=1)
    user_image = models.ImageField(upload_to=user_directory_path)
    resume = models.FileField(upload_to=user_dir_path)
    registration_date = models.DateField(auto_now_add=True)
    activation_code = models.TextField(max_length=50, default=None, null=True)
    account_activated = models.TextField(max_length=10, default=False)


class UserLog(models.Model):
    user_acc_id = models.IntegerField()
    last_login_date = models.DateField(auto_now_add=True)
    last_job_apply = models.DateField(auto_now_add=True)


class JobPost(models.Model):
    post_id = models.IntegerField(primary_key=True, auto_created=True)
    posted_by_email = models.EmailField()
    created_date = models.DateField(auto_now_add=True)
    job_title = models.TextField(max_length=30)
    job_description = models.TextField(max_length=500)
    job_location = models.TextField(max_length=20)
    job_type = models.TextField(max_length=10, null=True)
    job_skills = models.TextField(max_length=10, null=True)
    is_active = models.IntegerField(default=1)


class JobPostActivity(models.Model):
    email = models.EmailField(null=False)
    post_id = models.IntegerField(null=False)
    apply_date = models.DateField(auto_now_add=True)

