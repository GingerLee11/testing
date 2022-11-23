from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from accounts import views

urlpatterns = [
    path('send_login_email', views.send_login_email, name='send-login-email'),
    path('login', views.login, name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
