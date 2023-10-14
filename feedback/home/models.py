from django.db import models

# Create your models here.
class Video(models.Model):
    name = models.CharField(max_length=256,default='video')
    video = models.FileField(upload_to="%y/")