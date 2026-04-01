from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from files.models import Folder, UploadedFile
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()
            return redirect('accounts:signin')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        user_identity = request.POST['user_identity']
        password = request.POST['password']

        try:
            if user_identity.endswith('@gmail.com'):
                user_obj = User.objects.get(email=user_identity)
                user = authenticate(request, username=user_obj.username, password=password)

            else:
                user = authenticate(request, username=user_identity, password=password)
            
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('files:dashboard')
        
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'accounts/signin.html')


def signout(request):
    logout(request)
    return redirect('accounts:signin')


def my_profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        user.save()
        
        return redirect('accounts:my_profile')
    

    files = UploadedFile.objects.filter(user=user)
    folders = Folder.objects.filter(user=user)
    favorites = UploadedFile.objects.filter(user=user, is_favourite=True)

    context = {
        'files': files,
        'folders': folders,
        'favorites': favorites
    }

    return render(request, 'accounts/userprofile.html', context)


def settings(request):

    if request.method == 'POST':

        if 'clear_data' in request.POST:
            UploadedFile.objects.filter(user=request.user).delete()
            return redirect('accounts:my_profile')
        
        if 'delete_account' in request.POST:
            user = request.user
            logout(request)   # logout first
            user.delete()     # then delete account
            return redirect('home')
        
    return render(request, 'accounts/settings.html')


def change_password(request):

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if new_password != confirm_password:
            print("New passwords do not match.")
            messages.error(request, "New passwords do not match.")
            return redirect('accounts:my_profile')

        if current_password == new_password:
            print("New password cannot be same as current password.")
            messages.warning(request, "New password cannot be same as current password.")
            return redirect('accounts:my_profile')
        
        if not user.check_password(current_password):
            print("Current password is incorrect.")
            messages.error(request, "Current password is incorrect.")
            return redirect('accounts:my_profile')
            
        user.set_password(new_password)
        user.save()
        logout(request)

        messages.success(request, "Password changed successfully. Please login again.")
        return redirect('accounts:signin')

    return redirect('accounts:my_profile') 