from django.db.models import Q
from .models import *


def searchProjects(request):
    search_query = ''
    # Search
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    # print('SEARCH:', search_query)
    
    tags = Tag.objects.filter(name__icontains=search_query)
    
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) | 
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    
    return projects, search_query