from django.urls import path
from users import views as views

urlpatterns = [
    path('home', views.home, name='Home'),
    path('cadastro', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('cadastro/2', views.PersonalProfileInformation.as_view(), name='signup2'),
    path('profile/<int:id>/edit', views.PersonalProfileInformation.as_view(), name='profile_edit'),
]