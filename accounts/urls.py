from django.urls import path
from .import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),

    path('my_profile/', views.my_profile, name='my_profile'),
    path('settings/', views.settings, name='settings'),
    path('change_password/', views.change_password, name='change_password'),

    path('verify-otp/', views.verify_otp, name='verify_otp'),

    path('send-otp/', views.send_otp, name='send_otp'),
    path('forgot-password-verify-otp/', views.forgot_password_verify_otp, name='forgot_password_verify_otp'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]
