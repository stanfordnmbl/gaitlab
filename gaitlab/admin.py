from django.contrib import admin
from gaitlab.models import Video, Annotation

class AnnotationAdmin(admin.ModelAdmin):
    pass
class VideoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Video, VideoAdmin)
