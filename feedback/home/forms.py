from django import forms
from .models import Video

class Video_form(forms.ModelForm):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={
            'class': 'styled-input',
            'placeholder': 'Enter your name'
        })
    )
    video = forms.FileField(
        label="Video",
        widget=forms.ClearableFileInput(attrs={'class': 'styled-input'})
    )
    class Meta:
        model = Video
        fields = ('name', 'video')