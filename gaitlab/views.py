from django.shortcuts import render
from django.http import HttpResponse
from gaitlab.forms import VideoForm
from django.forms.widgets import ClearableFileInput
from django.shortcuts import redirect
from gaitlab.models import Video, Annotation
from gaitlab import celery_app
from django.views.decorators.csrf import csrf_exempt
import json

map_gmfcs = {
    0: "I",
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "IV",
}

map_key_names = {
    "gmfcs": "GMFCS",
    "SEMLS_dev_residual": "SEMLS indication",
    "KneeFlex_maxExtension_L": "Left knee flex. at max extension",
    "KneeFlex_maxExtension_R": "Right knee flex. at max extension",
}

map_units = {
    "speed": "m/s",
    "cadence": "strides/s",
    "KneeFlex_maxExtension_L": "degrees",
    "KneeFlex_maxExtension_R": "degrees",
}

def analysis(request, slug):
    video = Video.objects.get(slug=slug)
    annotations = video.annotation_set.all()
    annotation = None
    if annotations.count() > 0:
        annotation = annotations[0]

    # convert to int
    results = annotation.response
    results["GDI"] = int(results["GDI"])
    results["gmfcs"] = map_gmfcs.get(int(results["gmfcs"]),"N/A")

    # convert to 2 decimals
    for key in ["speed","cadence","SEMLS_dev_residual","KneeFlex_maxExtension_L","KneeFlex_maxExtension_R"]:
        results[key] = round(float(results[key]), 2)

    # add units
    for key in map_units.keys():
        results[key] = "{} {}".format(results[key], map_units[key])
    

    # fix names 
    keys = list(results.keys())
    for key in keys:
        if key not in map_key_names.keys():
            continue
        val = results[key]
        del results[key]
        results[map_key_names[key]] = val
    
    return render(request, 'gaitlab/analysis.html', {
        "video": video,
        "annotation": annotation,
        "results": results,
    })

def index(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            ann = Annotation(video=obj)
            ann.save()
            celery_app.send_task("gaitlab.cp", ({
                "annotation_id": ann.id,
                "video_url": obj.file.url
            }, ))
            return redirect(obj)
    else:
        form = VideoForm()
        
    form.fields["file"].widget.attrs['accept'] = 'video/*;capture=camera'

    return render(request, 'gaitlab/index.html', { "form": form })

@csrf_exempt
def annotation_update(request, id):
    ann = Annotation.objects.get(id=id)
    ann.file.save(request.FILES["file"].name, request.FILES["file"])

    print(request.POST["result"])
    ann.response = json.loads(request.POST["result"])
    ann.status = "done"
    ann.save()
    return HttpResponse("Done")
