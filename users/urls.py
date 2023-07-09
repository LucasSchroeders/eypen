from django.urls import path
from .views import views

urlpatterns = [
    path('home', views.home, name='Home'),
    path('cadastro', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('profile/company', views.ProfileCompany.as_view(), name='profile_company'),
]