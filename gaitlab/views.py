from django.shortcuts import render
from django.http import HttpResponse
from gaitlab.forms import VideoForm
from django.forms.widgets import ClearableFileInput
from django.shortcuts import redirect
from gaitlab.models import Video

def analysis(request, slug):
    video = Video.objects.get(slug=slug)
    
    return render(request, 'gaitlab/analysis.html', { "video": video })

def index(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return redirect(obj)
    else:
        form = VideoForm()
        
    form.fields["file"].widget.attrs['accept'] = 'video/*;capture=camera'

    return render(request, 'gaitlab/index.html', { "form": form })

