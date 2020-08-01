from django.forms import ModelForm
from gaitlab.models import Video
from django import forms

class VideoForm(ModelForm):
    terms_confirmed = forms.BooleanField(label="I've read and accept the terms of use.")
    
    class Meta:
        model = Video
        fields = ["file"]
