from django.db import models
import jsonfield
from randomslugfield import RandomSlugField
from django.urls import reverse

STATUS_CHOICES = [
    ("submitted","Submitted"),
    ("processing","Processing"),
    ("done","Done"),
    ("error","Error"),
]

class Video(models.Model):
    slug = RandomSlugField(length=8)
    file = models.FileField()
    email = models.EmailField(null=True)

    def get_absolute_url(self):
        return reverse('analysis', args=[str(self.slug)])

class Annotation(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    file = models.FileField(null=True)
    response = jsonfield.JSONField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')
