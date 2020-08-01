from django.contrib import admin
from gaitlab.models import Video, Annotation

class AnnotationAdmin(admin.ModelAdmin):
    pass

class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ["slug",]
    fields = ["slug","file","email",]


admin.site.register(Annotation, AnnotationAdmin)
admin.site.register(Video, VideoAdmin)
