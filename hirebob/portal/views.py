import uuid
from django.shortcuts import render
from .forms import FormUserCreation, FormLogin, FormJobPost
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import UserAccount, JobPost
from django.shortcuts import redirect
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
            'name': request.session["name"]}

    return render(request, 'pages/profile_org.html', data)


def post_job(request):
    data = {"header_name": "Post Jobs",
            'email': request.session["email"],
            'form': FormJobPost(initial={'posted_by_email': request.session["email"]}),
            'name': request.session["name"]}

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
            'name': request.session["name"]}
    return render(request, 'pages/profile_applicant.html', data)


def show_jobs(request):
    data = {"header_name": "Organization Page",
            'email': request.session["email"],
            'name': request.session["name"]}
    if request.method == "GET":
        job_post_obj = JobPost.objects.all()
        data["data"] = job_post_obj
    return render(request, 'pages/jobs.html', data)


def applied_jobs(request):
    data = {"header_name": "Organization Page",
            'email': request.session["email"],
            'name': request.session["name"]}
    return render(request, 'pages/applied_jobs.html', data)


def applicants_list(request):
    data = {"header_name": "applicants list",
            'email': request.session["email"],
            'name': request.session["name"]}

    return render(request, 'pages/applicants_list_org.html', data)


def job_details(request, email, id):
    data = {"header_name": "applicants list",
            'email': request.session["email"],
            'name': request.session["name"]}
    job_post_obj = JobPost.objects.filter(post_id=id)
    data["data"] = job_post_obj
    return render(request, 'pages/job_details.html', data)
