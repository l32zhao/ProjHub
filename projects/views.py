from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import ProjectForm

# Create your views here.

def projects(request):  # A view
    # return HttpResponse('Here are our products.')
    # page = "PROJECTS"
    # number = 10
    # context = {'page':page, 'number':number}
    # return render(request, 'projects/projects.html', context)
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)


def project(request, pk):  # A view
    # return HttpResponse('Single project: '+pk)
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'project': projectObj})
    

# CRUD
@login_required(login_url="login")  # Authentication
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()    # Init project fields
    
    if request.method == 'POST':
        # print(request.POST)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid(): # Check valid
            project = form.save(commit=False)
            project.owner = profile     # One to many relationship
            project.save()
            return redirect('projects') # redirect to user
        
    context = {'form': form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def updateProject(request, pk): # need a primary key
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid(): # Check valid
            form.save()
            return redirect('projects') # redirect to user
        
    context = {'form': form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def deleteProject(request, pk): # need a primary key
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    # context is a object
    context = {'object': project}
    
    return render(request, "projects/delet_template.html", context)