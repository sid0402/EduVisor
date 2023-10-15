from django.db import models

# Create your models here.
class Lectures(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256, default="Previous Lecture")
    engagement_ratio = models.DecimalField(decimal_places=2,max_digits=5)
    tone_modality = models.DecimalField(decimal_places=2,max_digits=5)
    questions = models.DecimalField(decimal_places=2,max_digits=5)
    suggestion = models.TextField(default="")
    wpm = models.DecimalField(decimal_places=2,max_digits=5,default=0)