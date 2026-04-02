from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('files:dashboard')

    return render(request, 'cloudstore/home.html')