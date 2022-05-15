from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Jobs, User, References
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required



@login_required(login_url='/auth/login')
def find_jobs(request):
    if request.method == 'GET':
        lowest_price = request.GET.get('lowest_price')
        highest_price = request.GET.get('highest_price')
        short_date = request.GET.get('short_date')
        long_date = request.GET.get('long_date')
        category = request.GET.get('category')

        if any([lowest_price, highest_price, short_date, long_date, category]):
            if not lowest_price:
                lowest_price = 0
            if not highest_price:
                highest_price = 999999
            if not short_date:
                short_date = datetime(year=1900, month=1, day=1)    
            if not long_date:
                long_date = datetime(year=3000, month=12, day=31)

            if category == 'VE':
                category = ['VE']
            if category == 'D':
                category = ['D']
            if category == 'ALL':
                category = ['VE', 'D']
            

            jobs = Jobs.objects.filter(reserved=False)\
                                .filter(price__gte=lowest_price)\
                                .filter(price__lte=highest_price)\
                                .filter(deadline__gte=short_date)\
                                .filter(deadline__lte=long_date)\
                                .filter(category__in=category)


        else:
            jobs = Jobs.objects.filter(reserved=False)
        
        return render(request, 'find_jobs.html', context={'jobs': jobs})

@login_required(login_url='/auth/login')
def get_job(request, id):
    job = Jobs.objects.get(id=id)
    job.reserved = True
    job.professional = request.user
    job.save()
    return redirect('/jobs/find_jobs')
    
@login_required(login_url='/auth/login')
def profile(request):
    if request.method == 'GET':
        jobs = Jobs.objects.filter(professional=request.user)
        return render(request, 'profile.html', context={'jobs': jobs})
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = User.objects.filter(username=username).exclude(id=request.user.id)

        if user.exists():
            messages.add_message(request, constants.ERROR, "User already exists.")
            return redirect('/jobs/profile')

        user = User.objects.filter(email=email).exclude(id=request.user.id)

        if user.exists():
            messages.add_message(request, constants.ERROR, "Email already exists.")

        request.user.username = username
        request.user.email = email
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        messages.add_message(request, constants.SUCCESS, "Profile updated!")
        return redirect('/jobs/profile')

# Called when user send his file
@login_required(login_url='/auth/login')
def send_work(request):
    job_id = request.POST.get('id')
    job = Jobs.objects.get(id=job_id)
    job.work_file = request.FILES.get('work_file')
    job.status = 'WA'
    job.save()
    return redirect('/jobs/profile')

# TODO create error messages
@login_required(login_url='/auth/login')
def create_job(request):
    if request.method == 'GET':
        return render(request, 'create_job.html')
    
    if request.method == 'POST':
        print(request.POST.get('deadline'))

        new_reference = References()
        new_reference.file = request.FILES.get('file')
        new_reference.save()

        new_job = Jobs()
        new_job.title = request.POST.get('title')
        new_job.description = request.POST.get('description')
        new_job.category = request.POST.get('category')
        new_job.deadline = request.POST.get('deadline')
        new_job.price = request.POST.get('price')
        new_job.creator = request.user                                      
        new_job.save()

        new_job.references.add(new_reference)

        return redirect('/jobs/find_jobs')

# TODO create error messages
@login_required
def update_job(request, job_id):
    if request.method == 'GET':
        job = Jobs.objects.get(id=job_id)
        return render(request, 'update_job.html', context={'job': job})
    
    if request.method == 'POST':
        job = Jobs.objects.get(id=request.POST.get('job_id'))

        if request.FILES.get('file'):
            new_reference = References()
            new_reference.file = request.FILES.get('file')
            new_reference.save()
            job.references.add(new_reference)

        price = request.POST.get('price').replace(',', '.')

        job.price = price
        job.title = request.POST.get('title')
        job.description = request.POST.get('description')
        job.category = request.POST.get('category')
        job.deadline = request.POST.get('deadline')
        job.save()

        return redirect('/jobs/find_jobs')
