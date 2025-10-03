from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as authorize, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.db.models import Count, Q
from .forms import SignUpForm, LoginForm, addApplicationForm, editApplicationForm, ForgotPasswordRequestForm, ResetPasswordForm
from .models import JobApplications
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully! You may now login.")
            return redirect ('/')
        else:
            messages.error(request, 'Something went wrong while creating user.')
    else:
        form = SignUpForm()
        
    return render(request, 'auth/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST, use_required_attribute=False)
        if form.is_valid():
            user = form.get_user()
            authorize(request, user)
            return redirect('/dashboard')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})

from django.db.models import Count, Q

from django.core.paginator import Paginator

@login_required(login_url='/')
def home(request):
    if request.user.is_superuser:
        return HttpResponseForbidden("Admins cannot access this page.")
    
    all_jobs = JobApplications.objects.filter(user=request.user)
    
    # Calculate stats on all jobs
    stats = all_jobs.aggregate(
        total_jobs=Count('id'),
        total_offers=Count('id', filter=Q(status='Offered')),
        total_pending=Count('id', filter=Q(status='Pending')),
        total_noresponse=Count('id', filter=Q(status='No Response')),
        total_accepted=Count('id', filter=Q(status='Accepted')),
        total_rejected=Count('id', filter=Q(status='Rejected')),
    )
    
    # Order jobs for pagination
    jobs_ordered = all_jobs.order_by('-application_date')
    
    # Paginate with 5 items per page
    paginator = Paginator(jobs_ordered, 5)
    page_number = request.GET.get('page', 1)
    jobs = paginator.get_page(page_number)
    
    form = addApplicationForm()
    
    for job in jobs:
        job.edit_form = editApplicationForm(instance=job)

    context = {
        'username': request.user.username,
        'total_jobs': stats['total_jobs'],
        'total_offers': stats['total_offers'],
        'total_noresponse': stats['total_noresponse'],
        'total_pending': stats['total_pending'],
        'total_accepted': stats['total_accepted'],
        'total_rejected': stats['total_rejected'],
        'jobs': jobs,
        'form': form,        
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='/')
def add_application(request):
    if request.method == "POST":
        form = addApplicationForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            messages.success(request, 'Job Application Added')
        else:
            messages.error(request, 'Error inserting job application.')

    return redirect('/dashboard')

def search_application(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        jobs = (
            JobApplications.objects
            .filter(user=request.user)
            .filter(
                Q(company__icontains=query) |
                Q(job_name__icontains=query) |
                Q(job_desc__icontains=query) |
                Q(status__icontains=query)
            )
            .order_by('-application_date')[:5]
        )
    else:
        # When no query, return the latest items similar to dashboard default
        jobs = (
            JobApplications.objects
            .filter(user=request.user)
            .order_by('-application_date')[:5]
        )

    results = list(jobs.values(
        'id',
        'job_name',
        'job_desc',
        'company',
        'status',
        'application_date'
    ))

    return JsonResponse({'results': results})

@login_required(login_url='/')
def edit_application(request, id):
    job = get_object_or_404(JobApplications, pk=id, user=request.user)
   
    if request.method == "POST":
        form = editApplicationForm(request.POST, instance=job)
        if form.is_valid():
            if form.changed_data:
                instance = form.save(commit=False)
                instance.save(update_fields=form.changed_data)
                messages.success(request, 'Job Application Updated.')
            else:
                messages.info(request, 'No changes were made.')
        else:
            messages.error(request, 'Error updating Job Application')
    return redirect('/dashboard')

@login_required(login_url='/')
def delete_application(request, id):
    if request.method == "POST":
        job = get_object_or_404(JobApplications, pk=id, user=request.user)
        job.delete()
        messages.success(request, 'Job Application Deleted')
    return redirect('/dashboard')

@login_required(login_url='/')
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
def profile(request):
    show_password_form = False
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'password':
            show_password_form = True
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if not old_password or not request.user.check_password(old_password):
                messages.error(request, "Current password is incorrect.")
                return render(request, 'profile/profile.html', {'show_password_form': show_password_form})
            
            if new_password1 != new_password2:
                messages.error(request, "New passwords don't match!")
                return render(request, 'profile/profile.html', {'show_password_form': show_password_form})
            
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Password updated.')
            return redirect('profile')
        
        elif form_type == 'profile':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            changed = False
            
            if first_name is not None and first_name != request.user.first_name:
                request.user.first_name = first_name
                changed = True
            if last_name is not None and last_name != request.user.last_name:
                request.user.last_name = last_name
                changed = True
            if email is not None and email != request.user.email:
                request.user.email = email
                changed = True
            
            if changed:
                request.user.save()
                messages.success(request, 'Profile updated successfully.')
            else:
                messages.info(request, 'No changes were made.')
            return redirect('profile')
    
    return render(request, 'profile/profile.html')


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Find users with this email. Do not reveal existence in UI.
            users = User.objects.filter(email__iexact=email)
            for user in users:
                token_generator = PasswordResetTokenGenerator()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                )
                subject = 'Reset your CareerQuest password'
                message = render(request, 'auth/password_reset_email.txt', {
                    'user': user,
                    'reset_url': reset_url,
                }).content.decode('utf-8')
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    logger.exception("Password reset email failed to send: %s", e)
                    
            messages.success(request, 'If an account with that email exists, a reset link has been sent.')
            return redirect('login')
    else:
        form = ForgotPasswordRequestForm()
    return render(request, 'auth/forgot_password.html', {'form': form})


def reset_password_confirm(request, uidb64, token):
    token_generator = PasswordResetTokenGenerator()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is None or not token_generator.check_token(user, token):
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect('login')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset. You can now log in.')
            return redirect('login')
    else:
        form = ResetPasswordForm()

    return render(request, 'auth/reset_password_confirm.html', {'form': form})