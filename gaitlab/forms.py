from django.forms import ModelForm
from gaitlab.models import Video

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ["file"]
