from django.shortcuts import render


def home(request):
    return render(request, 'progress_tracking/home.html')
