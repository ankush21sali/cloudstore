from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import secrets

from django.contrib.auth.models import User
from .models import OTP


def generate_otp():
    return "".join(str(secrets.randbelow(10)) for _ in range(6))


def send_otp_email(email):

    otp_code = generate_otp()

    user = User.objects.get(email=email)

    OTP.objects.update_or_create(
        user=user,
        defaults={
            "otp": otp_code,
            "expires_at": timezone.now() + timedelta(minutes=5)
        }
    )

    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP is {otp_code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )
        