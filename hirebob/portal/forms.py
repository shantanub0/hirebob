from django import forms
from .models import UserAccount, JobPost, JobPostActivity


class FormUserCreation(forms.ModelForm):
    UserTypes = ((1, 'Applicants'), (2, 'Organisations'))
    user_type = forms.ChoiceField(choices=UserTypes,
                                  widget=forms.Select(attrs={'class': "form-control"}))
    user_full_name = forms.CharField(max_length=100,
                                     widget=forms.TextInput(attrs={'class': "form-control",
                                                                   'placeholder': 'Enter Full Name'}))
    email = forms.EmailField(max_length=250,
                             help_text="Required. Invalid format",
                             widget=forms.TextInput(attrs={'class': "form-control",
                                                           'placeholder': 'Enter Email ID'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",
                                                             'type': 'password',
                                                             'placeholder': 'Enter Password',
                                                             'minlength': '6',
                                                             'onkeyup': 'check();'}))
    confirm_password = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",
                                                                     'type': 'password',
                                                                     'placeholder': 'Re-enter Password',
                                                                     'minlength': '6',
                                                                     'onkeyup': 'check();'}))
    class Meta:
        model = UserAccount
        fields = ('user_type', 'user_full_name', 'email', 'password')


class FormLogin(forms.ModelForm):
    email = forms.EmailField(max_length=250,
                             help_text="Required. Invalid format",
                             widget=forms.TextInput(attrs={'class': "form-control",
                                                           'placeholder': 'Enter Email ID'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",
                                                             'type': 'password',
                                                             'placeholder': 'Enter Password',
                                                             'minlength': '6'}))
    class Meta:
        model = UserAccount
        fields = ('email', 'password')


class FormJobPost(forms.ModelForm):
    Locations = (('Mumbai', 'Mumbai'), ('Navi Mumbai', 'Navi Mumbai'), ('Pune', 'Pune'))
    job_types = (('Software Engineer', 'Software Engineer'), ('Database Admin', 'Database Admin'), ('DevOps', 'DevOps'))
    jobs_skill = (('Java', 'Java'), ('Python', 'Python'), ('C', 'C'), ('C++', 'C++'))

    job_location = forms.ChoiceField(choices=Locations,
                                     widget=forms.Select(attrs={'class': "form-control"}))
    job_type = forms.ChoiceField(choices=job_types,
                                 widget=forms.Select(attrs={'class': "form-control"}))
    job_skills = forms.ChoiceField(choices=jobs_skill,
                                     widget=forms.Select(attrs={'class': "form-control"}))

    job_title = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'class': "form-control",
                                                              'placeholder': 'Enter job title'}))

    posted_by_email = forms.EmailField(max_length=250,
                                       help_text="Required. Invalid format",
                                       widget=forms.TextInput(attrs={'class': "form-control",
                                                              'placeholder': 'Enter Email ID',
                                                              'readonly': True}))
    job_description = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control", 'placeholder': 'Enter Full Name'}))

    class Meta:
        model = JobPost
        fields = ('job_type', 'job_skills', 'job_location', 'posted_by_email', 'job_description', 'job_title')


class FormApply(forms.ModelForm):
    email = forms.EmailField(required=True,
                             max_length=250,
                             help_text="Required. Invalid format",
                             widget=forms.TextInput(attrs={'class': "form-control",
                                                           'placeholder': 'Enter Email ID',
                                                           'readonly': True}))
    to_email = forms.EmailField(required=True,
                                max_length=250,
                                help_text="Required. Invalid format",
                                widget=forms.TextInput(attrs={'class': "form-control",
                                                              'placeholder': 'Enter Email ID',
                                                              'readonly': True}))
    cover_letter = forms.CharField(required=True,
                                   widget=forms.Textarea(attrs={'class': "form-control",
                                                                'placeholder': 'Enter Full Name'}))

    post_id = forms.IntegerField(required=True,
                                 widget=forms.TextInput(attrs={'class': "form-control",
                                                               'placeholder': 'Post ID',
                                                               'readonly': True}))
    job_title = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': "form-control",
                                                              'placeholder': 'Enter Full Name'}))

    class Meta:
        model = JobPostActivity
        fields = ('email', 'post_id')


class FormUploadImage(forms.Form):
    user_image = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = UserAccount
        fields = ('user_image', )


class FormUploadResume(forms.Form):
    resume = forms.FileField()

    class Meta:
        model = UserAccount
        fields = ('resume', )
