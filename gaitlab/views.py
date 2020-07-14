from django.shortcuts import render
from django.http import HttpResponse
from gaitlab.forms import VideoForm
from django.forms.widgets import ClearableFileInput
from django.shortcuts import redirect
from gaitlab.models import Video, Annotation
from gaitlab import celery_app

def analysis(request, slug):
    video = Video.objects.get(slug=slug)
    annotations = video.annotation_set.all()
    annotation = None
    if annotations.count() > 0:
        annotation = annotations[0]
    
    return render(request, 'gaitlab/analysis.html', { "video": video, "annotation": annotation })

def index(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            ann = Annotation(video=obj)
            ann.save()
            celery_app.send_task("gaitlab.cp", ({"annotation_id": ann.id, "video_url": obj.file.url}, ))
            return redirect(obj)
    else:
        form = VideoForm()
        
    form.fields["file"].widget.attrs['accept'] = 'video/*;capture=camera'

    return render(request, 'gaitlab/index.html', { "form": form })

