from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import JobApplications

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
        widget=forms.TextInput(attrs={'id': 'username'})
    )
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Input a valid email address.',
        widget=forms.EmailInput(attrs={'id': 'email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password1'}),
        label="Password:"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password2'}),
        label="Confirm Password:"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        placeholder_values = {
            'username': 'Enter a username',
            'email': 'Enter your email',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if field_name in placeholder_values:
                field.widget.attrs['placeholder'] = placeholder_values[field_name]

            # Remove HTML5 required attribute
            field.required = False
            field.widget.attrs.pop('required', None)


class LoginForm(AuthenticationForm):

    def clean(self):
        
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            # Find user by email first
            if '@' in username_or_email and password:
                try:
                    user = User.objects.get(email=username_or_email)
                    username = user.username
                except User.DoesNotExist:
                    username = username_or_email
            else:
                username = username_or_email

            self.user_cache = authenticate(
                self.request,
                username = username,
                password = password
            )

            if self.user_cache is None:
                raise forms.ValidationError("Invalid Username/Email or Password.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    
    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(request, *args, **kwargs)

        self.fields['username'].label = "Username or Email:"
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter Username or Email',
            'id': 'usernameOrEmail',
            'class': 'form-control'
        })

        self.fields['password'].label = "Password:"
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Enter password',
            'id': 'password',
            'class': 'form-control'
        })

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class addApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplications
        fields = ['company', 'job_name', 'job_desc', 'status', 'application_date']

    def __init__(self, *args, **kwargs):
        super(addApplicationForm, self).__init__(*args, **kwargs)

        self.fields['company'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Name of Company'})
        self.fields['job_name'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Position/Title'})
        self.fields['job_desc'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Job Description'})
        self.fields['status'].widget = forms.Select(choices=[('', '--- Select Status ---'), ('Accepted', 'Accepted'),  ('No Response', 'No Response'), ('Offered', 'Offered'), ('Pending', 'Pending'),('Rejected', 'Rejected')])
        self.fields['status'].widget.attrs.update({ 'class': 'form-select' })
        self.fields['application_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['application_date'].widget.attrs.update({ 'class': 'form-control' })


class editApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplications
        fields = ['company', 'job_name', 'job_desc', 'status', 'application_date']
        
    def __init__(self, *args, **kwargs):
        super(editApplicationForm, self).__init__(*args, **kwargs)

        self.fields['company'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Name of Company'})
        self.fields['job_name'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Position/Title'})
        self.fields['job_desc'].widget.attrs.update({ 'class': 'form-control', 'placeholder': 'Job Description'})
        self.fields['status'].widget = forms.Select(choices=[('', '--- Select Status ---'), ('Accepted', 'Accepted'),  ('No Response', 'No Response'), ('Offered', 'Offered'), ('Pending', 'Pending'),('Rejected', 'Rejected')])
        self.fields['status'].widget.attrs.update({ 'class': 'form-select' })
        self.fields['application_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['application_date'].widget.attrs.update({ 'class': 'form-control' })