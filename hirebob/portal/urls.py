from django.conf.urls import url
from . import views

urlpatterns = [
    url('^template/', views.template, name='template'),

    # Sign Up
    url(r'^$|^sign-up/', views.sign_up, name='sign_up'),
    url(r'^email_activation/(?P<activation>[\w-]+)/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/$',
        views.email_activation, name='email_activation'),

    # Login
    url(r'^sign-in/', views.sign_in, name='sign_in'),
    url(r'^sign-out/', views.logout, name='sign-out'),

    # Org user
    url(r'^org-user/', views.organization, name='org_user'),
    url(r'^post-job/', views.post_job, name='post_job'),
    url(r'^applicants-list/', views.applicants_list, name='applicants-list'),
    url(r'^job_details/(?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)/(?P<id>[\d]+)/', views.job_details,
        name="job_details"),

    # applicant user
    url(r'^applicant/', views.applicant, name='applicant'),
    url(r'^show_jobs/', views.show_jobs, name='show_jobs'),
    url(r'^applied_jobs/', views.applied_jobs, name='applied_jobs'),
]
