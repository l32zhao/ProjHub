from django.forms import ModelForm
from django import forms
from .models import Project

class ProjectForm(ModelForm):
    class Meta: # at least 2 things
        model = Project
        # fields = '__all__'    # all fields
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link', 'tags']
        
        widgets = {     # Style
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__()
        
        
        for name, field in self.fields.items(): # Style
            field.widget.attrs.update({'class':'input'})
        # self.fields['title'].widget.attrs.update({'class':'input'}) # Overwrite
        
        # self.fields['description'].widget.attrs.update({'class':'input'}) # Overwrite