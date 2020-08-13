from django.forms import ModelForm
from gaitlab.models import Video
from django import forms
from django.utils.safestring import mark_safe

class VideoForm(ModelForm):
    terms_confirmed = forms.BooleanField(label=mark_safe("I've read and accept <a href='#license'>the terms of use</a>."))
    
    class Meta:
        model = Video
        fields = ["file"]
