from django.shortcuts import render,HttpResponse, redirect
from .models import Video
from .forms import Video_form

# Have to display video on home page
def home(request):
    if (request.method == "POST"):
        print(request.FILES)
        form = Video_form(data=request.POST,files = request.FILES)
        if form.is_valid():
            form.save()
            return redirect(success)
    else:
        form = Video_form()
    context = {'form':form}
    return render(request,'home/home.html',context)

def success(request):
    filename = 'media/'+str(Video.objects.all()[len(Video.objects.all())-1].video)
    name = Video.objects.all()[len(Video.objects.all())-1].name
    context = {'video':filename,'name':name}
    return render(request, 'home/success.html',context)