from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from files.models import Folder, UploadedFile
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from datetime import timedelta
from .models import OTP
from.utils import send_otp_email

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            
            user.is_active = False
            user.save()

            # Store ID in session so verify_otp can find this user.
            request.session['user_id'] = user.id 

            send_otp_email(user.email)
            messages.info(request, "Please check your email for the OTP.")
            return redirect('accounts:verify_otp')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        user_identity = request.POST['user_identity']
        password = request.POST['password']
        
        if user_identity.endswith('@gmail.com'):
            user_obj = User.objects.filter(email=user_identity).first()
        else:
            user_obj = User.objects.filter(username=user_identity).filter()

        if user_obj and user_obj.check_password(password):

            if not user_obj.is_active:
                request.session['user_id'] = user_obj.id
                send_otp_email(user_obj.email)

                messages.warning(request, "Account not verified. A new OTP has been sent.")
                return redirect('accounts:verify_otp')
            
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('files:dashboard')

        messages.error(request, "Invalid email or password")
        
    return render(request, 'accounts/signin.html')


def verify_otp(request):
    user_id = request.session.get("user_id")
    
    if not user_id:
        messages.error(request, "Session expired. Please sign up again.")
        return redirect("accounts:signup")

    if request.method == "POST":
        entered_otp = request.POST.get("code")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "Account not found. Please sign up.")
            return redirect("accounts:signup")
        
        otp_obj = OTP.objects.filter(user=user).last()

        if not otp_obj:
            messages.warning(request, "No OTP found")
            return redirect("accounts:verify_otp")

        if otp_obj.is_expired():
            otp_obj.delete()
            messages.warning(request, "OTP Expired")
            return redirect("accounts:verify_otp")

        if otp_obj.otp == entered_otp:
            user.is_active = True
            user.save()

            login(request, user)

            otp_obj.delete()
            del request.session["user_id"]

            messages.success(request, "OTP Verified Successfully")
            return redirect("files:dashboard")

        messages.error(request, "Invalid OTP")
        return redirect("accounts:verify_otp")

    return render(request, "accounts/verify-otp.html")


def signout(request):
    logout(request)
    return redirect('accounts:signin')


@login_required
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


@login_required
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


@login_required
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



def send_otp(request):

    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        messages.error(request, "Opps!, User DoesNotExist.")
        return redirect('accounts:my_profile')
    
    # Store ID in session so verify_otp can find this user.
    request.session['user_id'] = user.id 
    
    send_otp_email(user.email)
    messages.info(request, "Please check your email for the OTP.")
    return redirect('accounts:reset_password_verify_otp')



def reset_password_verify_otp(request):
    user_id = request.session.get("user_id")
    
    if not user_id:
        messages.error(request, "Session expired. Please try again later.")
        return redirect("files:dashboard")

    if request.method == "POST":
        entered_otp = request.POST.get("code")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "Account not found. Please try again later.")
            return redirect("files:dashboard")
        
        otp_obj = OTP.objects.filter(user=user).last()

        if not otp_obj:
            messages.warning(request, "No OTP found")
            return redirect("accounts:reset_password_verify_otp")

        if otp_obj.is_expired():
            otp_obj.delete()
            messages.warning(request, "OTP Expired")
            return redirect("accounts:reset_password_verify_otp")

        if otp_obj.otp == entered_otp:
            user.is_active = True
            user.save()

            login(request, user)

            otp_obj.delete()
            del request.session["user_id"]

            messages.success(request, "OTP Verified Successfully")
            return redirect("accounts:reset_password")

        messages.error(request, "Invalid OTP")
        return redirect("accounts:reset_password_verify_otp")

    return render(request, "accounts/reset_password_verify_otp.html")


@login_required
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('accounts:reset_password')
            
        user.set_password(new_password)
        user.save()
        logout(request)

        messages.success(request, "Password changed successfully. Please login again.")
        return redirect('files:dashboard')

    return render(request, "accounts/reset_password.html")


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Opps!, User DoesNotExist.")
            return redirect('accounts:signin')
        
        # Store ID in session so verify_otp can find this user.
        request.session['user_id'] = user.id 
        
        send_otp_email(user.email)
        messages.info(request, "Please check your email for the OTP.")
        return redirect('accounts:reset_password_verify_otp')

    return render(request, "accounts/forgot_password.html")