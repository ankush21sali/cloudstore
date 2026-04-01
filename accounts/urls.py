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
]
