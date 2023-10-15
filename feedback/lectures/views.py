from django.shortcuts import render, HttpResponse
from .models import Lectures
# Create your views here.
def home(request):
    lectures = Lectures.objects.all()
    for lecture in lectures:
        print(lecture.suggestion)
    context = {'lectures':lectures}
    return render(request, 'profile/home.html',context)