from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from .models import Video

class VideoAdminForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'
        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }