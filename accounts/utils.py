from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import requests
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

    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": "CloudStore",
            "email": settings.DEFAULT_FROM_EMAIL
        },
        "to": [{"email": user.email}],
        "subject": "Your OTP Code",
        "htmlContent": f"""
            <h2>Email Verification</h2>
            <p>Your OTP is: <strong>{otp_code}</strong></p>
            <p>This OTP expires in 5 minutes.</p>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.status_code)
    print(response.text)
        