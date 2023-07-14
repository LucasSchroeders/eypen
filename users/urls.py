from django.urls import path
from users import views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', views.home, name='Home'),
    path('cadastro', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('cadastro/2', views.signup2, name='signup2'),
    path('profile/<int:id>', views.PersonalProfileInformation.as_view(), name='profile_edit'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
