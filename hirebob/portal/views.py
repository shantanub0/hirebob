import os
import uuid
import re
import mimetypes
from django.shortcuts import render
from .forms import FormUserCreation, FormLogin, FormJobPost, FormApply, FormUploadImage, FormUploadResume, FormApplicantsInfo
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import UserAccount, JobPost, JobPostActivity, UserProfile
from django.shortcuts import redirect
from wsgiref.util import FileWrapper
from django.core import serializers


BASE_DIR = settings.BASE_DIR
HOST_NAME = settings.HOST_NAME
HOTS_PORT = settings.HOTS_PORT

# Create your views here.
def template(request):
    """
    Blank Template
    :param request:
    :return:
    """
    data = {"header_name": "Blank_Template",
            'email': request.session["email"]}
    if request.method == "GET":
        return render(request, 'pages/blank.html', data)


def sign_in(request, msg="Start your session!"):
    """
    Sign In function
    :param request:
    :param msg:
    :return:
    """

    data = {"header_name": "Sign In",
            "message": msg,
            "form": FormLogin}

    if request.method == "GET":
        try:
            del request.session['email']
            del request.session['name']
            del request.session['user_type']
        except Exception as ex:
            pass
        return render(request, 'pages/sign-in.html', data)
    elif request.method == "POST":
        form = FormLogin(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                user_account_obj = UserAccount.objects.get(email=email)
                if user_account_obj.password == password and user_account_obj.account_activated=="True":
                    request.session['email'] = email
                    request.session['name'] = user_account_obj.user_full_name
                    img_url = re.sub(r'portal', '', str(user_account_obj.user_image))
                    request.session['profile_img'] = img_url
                    request.session['user_type'] = user_account_obj.user_type
                    if user_account_obj.user_type == "1":
                        return redirect("show_jobs")
                    else:
                        return redirect("post_job")
                else:
                    data["message"] = "Login Failed"
            except Exception as ex:
                data["message"] = "Login Failed [%s]" % ex
        return render(request, 'pages/sign-in.html', data)


def sign_up(request):
    """
    User registration
    :param request:
    :return:
    """
    data = {"header_name": "Sign Up"}
    try:
        del request.session['email']
        del request.session['name']
        del request.session['user_type']
    except Exception as ex:
        pass
    data["form"] = FormUserCreation
    if request.method == "POST":
        form = FormUserCreation(request.POST)

        if form.is_valid():
            email = request.POST.get("email")
            try:
                user_account_obj = UserAccount.objects.get(email=email)
                if user_account_obj.email:
                    data["message"] = "User exist!"
                    return render(request, "pages/sign-up.html", data)
            except:
                pass

            try:
                result = form.save()
                if result:
                    activation = uuid.uuid4().hex

                    link = "http://" + HOST_NAME + ":" + str(HOTS_PORT) + "/portal/email_activation/" + activation + "/" + email
                    context = {"confirm_link": link}
                    message = render_to_string('email_templates/confirm_email.html', context)

                    # save uuid in db
                    user_account_obj = UserAccount.objects.get(email=email)
                    user_account_obj.activation_code = activation
                    user_account_obj.save()

                    send_mail(subject="Confirmation Email from HireBob",
                              message="",
                              from_email=settings.EMAIL_HOST_USER,
                              recipient_list=[email],
                              html_message=message)
                else:
                    raise Exception("Failed to save data")
                data["message"] = "Email send for account activation!"
            except Exception as ex:
                data["message"] = ex
            finally:
                return render(request, "pages/sign-up.html", data)
        else:
            return HttpResponse("Form is not valid")

    else:
        return render(request, 'pages/sign-up.html', data)


def email_activation(request, activation, email):
    """
    Email validation and account activation
    :param request:
    :param activation:
    :param email:
    :return:
    """
    message = "Failed to validate email"
    if request.method == "GET":
        user_account_obj = UserAccount.objects.get(email=email)
        if user_account_obj.activation_code == activation:
            user_account_obj.account_activated = True
            user_account_obj.save()
            message = "Account activated, Kindly login!"

        return redirect('sign_in')


def logout(request):
    """
    Clear login session and redirect to login page
    """

    try:
        del request.session['email']
    except KeyError:
        pass
    return redirect('sign_in')


def organization(request):
    data = {"header_name": "Organization Page",
            'email': request.session["email"],
            'name': request.session["name"],
            'profile_img': request.session["profile_img"],
            'imgform': FormUploadImage,
            'resumeform': FormUploadResume,
            'update_info': FormApplicantsInfo(initial={'email': request.session["email"]})}

    return render(request, 'pages/profile_org.html', data)


def post_job(request):
    data = {"header_name": "Post Jobs",
            'email': request.session["email"],
            'form': FormJobPost(initial={'posted_by_email': request.session["email"]}),
            'name': request.session["name"],
            'profile_img': request.session["profile_img"]}

    job_post_obj = JobPost.objects.filter(posted_by_email=request.session["email"])
    data["data"] = job_post_obj

    if request.method == "POST":
        form = FormJobPost(request.POST)
        if form.is_valid():
            form.save()
            data["message"] = "Job published "
        else:
            data["message"] = "Failed to publish job"
    else:
        data["message"] = "Publish Jobs"

    return render(request, 'pages/post_job.html', data)


def applicant(request):
    data = {"header_name": "Organization Page",
            'email': request.session["email"],
            'name': request.session["name"],
            'profile_img': request.session["profile_img"],
            'imgform': FormUploadImage,
            'resumeform': FormUploadResume,
            'update_info': FormApplicantsInfo(initial={'email': request.session["email"]})}
    try:
        user_acc_obj = UserAccount.objects.get(email=request.session["email"])
        img_url = re.sub(r'portal', '', str(user_acc_obj.user_image))
        data["img_url"] = img_url
        if "message" in request.session:
            data["message"] = request.session["message"]

    except Exception as ex:
        return redirect('sign_in')
    return render(request, 'pages/profile_applicant.html', data)


def show_jobs(request):
    data = {"header_name": "Organization Page",
            'email': request.session["email"],
            'name': request.session["name"],
            'profile_img': request.session["profile_img"]}
    if request.method == "GET":
        job_activity_obj = JobPostActivity.objects.filter(email=request.session["email"])
        job_applied = []
        for job in job_activity_obj:
            job_applied.append(job.post_id)

        job_post_obj = JobPost.objects.exclude(post_id__in=job_applied)
        data["data"] = job_post_obj
    return render(request, 'pages/jobs.html', data)


def applied_jobs(request):
    data = {"header_name": "Organization Page",
            'email': request.session["email"],
            'name': request.session["name"],
            'profile_img': request.session["profile_img"]}
    if request.method == "GET":
        job_activity_obj = JobPostActivity.objects.filter(email=request.session["email"])
        job_applied = []
        for job in job_activity_obj:
            job_applied.append(job.post_id)

        job_post_obj = JobPost.objects.filter(post_id__in=job_applied)
        data["data"] = job_post_obj
    return render(request, 'pages/jobs.html', data)
    # return render(request, 'pages/applied_jobs.html', data)


def applicants_list(request):
    data = {"header_name": "applicants list",
            'email': request.session["email"],
            'name': request.session["name"],
            'profile_img': request.session["profile_img"]}

    return render(request, 'pages/applicants_list_org.html', data)


def job_details(request, email, id):
    data = {"header_name": "applicants list",
            'email': request.session["email"],
            'name': request.session["name"],
            'applied': False,
            'profile_img': request.session["profile_img"]}
    job_post_obj = JobPost.objects.filter(post_id=id)
    data["data"] = job_post_obj
    data["form"] = FormApply(initial={'email': request.session["email"],
                                      'post_id': id,
                                      'to_email': job_post_obj[0].posted_by_email,
                                      'job_title': job_post_obj[0].job_title})
    try:
        job_activity_obj = JobPostActivity.objects.filter(post_id=id).filter(email=email)
        if job_activity_obj:
            data["applied"] = True
    except Exception as ex:
        pass
    return render(request, 'pages/job_details.html', data)


def apply(request):
    form = FormApply(request.POST)
    id = request.POST.get("post_id")
    if form.is_valid():
        job_title = request.POST.get("job_title")
        cover_letter = request.POST.get("cover_letter")
        email = request.session["email"]

        to_email = request.POST.get("to_email")
        link = "http://" + HOST_NAME + ":" + str(HOTS_PORT) + "/portal/user_profile/" + request.session["email"]
        org_context = {"job_link": link, "cover_letter": cover_letter, "title": "Application for %s " % job_title}
        applicant_context = {"title": "Application for %s " % job_title,
                             "email": to_email}

        form.save()

        org_message = render_to_string('email_templates/apply_job.html', org_context)
        applicant_message = render_to_string('email_templates/job_applied.html', applicant_context)

        # Celery implementation to send mail
        send_mail(subject="Applied for job %s " % job_title,
                  message="",
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[to_email],
                  html_message=org_message)

        send_mail(subject="Application has been sent to Organization",
                  message="",
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[email],
                  html_message=applicant_message)

    return redirect('job_details', email, id)


def upload_profile(request):
    if request.session["user_type"] == 1:
        out = 'applicant'
    else:
        out = 'org_user'
    form = FormUploadImage(request.POST,
                           request.FILES)
    if form.is_valid():
        user_acc_obj = UserAccount.objects.get(email=request.session["email"])
        user_acc_obj.user_image = form.cleaned_data["user_image"]
        user_acc_obj.save()
        img_url = re.sub(r'portal', '', str(user_acc_obj.user_image))
        request.session['profile_img'] = img_url

        return redirect(out)
    else:
        return redirect(out)


def upload_resume(request):
    form = FormUploadResume(request.POST,
                            request.FILES)
    if form.is_valid():
        user_acc_obj = UserAccount.objects.get(email=request.session["email"])
        user_acc_obj.resume = form.cleaned_data["resume"]
        user_acc_obj.save()
        return redirect('applicant')
    else:
        return redirect('applicant')


def download_resume(request, email):
    user_acc_obj = UserAccount.objects.get(email=email)
    filename = str(user_acc_obj.resume)
    donwload_filename = email + "_" + "resume"
    try:
        data = open(filename, "rb").read()
        response = HttpResponse(data, content_type='application/vnd.ms-word')
        response['Content-Disposition'] = 'attachment; filename=%s' % donwload_filename
        response['Content-Length'] = os.path.getsize(filename)
        return response
    except Exception as ex:
        return redirect('applicant')


def job_status(request, id):
    data = {"header_name": "applicants list",
            'email': request.session["email"],
            'name': request.session["name"],
            'applied': False,
            'profile_img': request.session["profile_img"]}

    job_activity = JobPostActivity.objects.filter(post_id=id)
    data["data"] = job_activity

    return render(request, "pages/job_status.html", data)


def user_profile(request, email):
    data = {"header_name": "applicants list",
            'email': request.session["email"],
            'name': request.session["name"],
            'applied': False,
            'profile_img': request.session["profile_img"]}
    try:
        data['user_type'] = request.session['user_type']
    except Exception as ex:
        data['user_type'] = ""
        pass
    user_acc_obj = UserAccount.objects.get(email=email)
    user_profile_obj = UserProfile.objects.get(email=email)
    data["data"] = user_acc_obj
    data["user_info"] = user_profile_obj
    img_url = re.sub(r'portal', '', str(user_acc_obj.user_image))
    data['img'] = img_url

    return render(request, "pages/user_profile.html", data)


def update_info(request):
    if request.session["user_type"] == 1:
        out = 'applicant'
    else:
        out = 'org_user'
    gender = request.POST.get("gender")
    email = request.POST.get("email")
    gmail = request.POST.get("gmail")
    linkedin = request.POST.get("linkedin")
    skype_id = request.POST.get("skype_id")
    about_me = request.POST.get("about_me")
    address = request.POST.get("address")
    birthday = request.POST.get("birthday")
    job_title = request.POST.get("job_title")
    location = request.POST.get("location")
    try:
        user_profile = UserProfile.objects.get(email=email)
        user_profile.gmail = gmail
        user_profile.gender = gender
        user_profile.linkedin = linkedin
        user_profile.skype_id = skype_id
        user_profile.about_me = about_me
        user_profile.address = address
        user_profile.birthday = birthday
        user_profile.job_title = job_title
        user_profile.location = location
        user_profile.save()
        request.session["message"] = "Information Updated"
        return redirect(out)
    except Exception as ex:
        user_profile = UserProfile.objects.create(email=email,
                                                  gender=gender,
                                                  gmail=gmail,
                                                  linkedin=linkedin,
                                                  skype_id=skype_id,
                                                  about_me=about_me,
                                                  address=address,
                                                  birthday=birthday,
                                                  job_title=job_title,
                                                  location=location)
        request.session["message"] = "Information added"
        return redirect(out)


def update_status(request, email, id, status):
    try:
        user_profile = JobPostActivity.objects.filter(email=email).filter(post_id=id).first()
        user_profile.status = status
        user_profile.save()
    except Exception as ex:
        pass

    context = {
        "title": "Job Status changed",
        "status": status,
        "email": request.session["email"]}
    message = render_to_string('email_templates/status_change.html', context)

    send_mail(subject="Job status changed to %s " % status,
              message="",
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[email],
              html_message=message)

    return redirect('job_status', id)
