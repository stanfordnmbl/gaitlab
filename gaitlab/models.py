from django.db import models
import jsonfield

STATUS_CHOICES = [
    ("submitted","Submitted"),
    ("processing","Processing"),
    ("done","Done"),
    ("error","Error"),
]

class Video(models.Model):
    file = models.FileField()
    email = models.EmailField()

class Annotation(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    file = models.FileField()
    response = jsonfield.JSONField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')
