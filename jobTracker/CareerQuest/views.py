from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as authorize, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Count, Q
from .forms import SignUpForm, LoginForm, addApplicationForm, editApplicationForm
from .models import JobApplications

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

@login_required(login_url='/')
def home(request):
    if request.user.is_superuser:
        return HttpResponseForbidden("Admins cannot access this page.")
    
    # Single query with aggregation
    jobs = JobApplications.objects.filter(user=request.user).order_by('-application_date')
    
    stats = jobs.aggregate(
        total_jobs=Count('id'),
        total_offers=Count('id', filter=Q(status='Offered')),
        total_pending=Count('id', filter=Q(status='Pending')),
        total_noresponse=Count('id', filter=Q(status='No Response')),
        total_accepted=Count('id', filter=Q(status='Accepted')),
        total_rejected=Count('id', filter=Q(status='Rejected')),
    )
    
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
    if request.method == 'POST':
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