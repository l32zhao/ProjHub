from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
from .models import *
from .forms import *

# Login/Logout
def loginUser(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist!')
        
        # Authentication
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)        # Add that into browser cookies
            return redirect('profiles') # to diff page
        else:
            messages.error(request, 'Username OR Password is incorrect!')
            
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request, 'User was logged out')
    return redirect('login')

# Register
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # tmp instance for modifyint it at front-end
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, 'User account was created!')
            
            login(request, user)
            return redirect('edit-account')
        
        else:
            messages.error(request, 'An error has occured during registration.')
        
    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    topSkills= profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    
    context = {'profile': profile,
               'topSkills': topSkills,
               'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    
    topSkills= profile.skill_set.all()
    # otherSkills = profile.skill_set.filter(description="")

    projects = profile.project_set.all()
    
    context = {'profile': profile,
               'skills': topSkills,
               'projects': projects,}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')
            
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)