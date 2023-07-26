from django.urls import path
from users import views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', views.home, name='Home'),
    path('cadastro', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('profile/company', views.ProfileCompany.as_view(), name='profile_company'),
    path('cadastro/2', views.signup2, name='signup2'),
    path('profile/<int:id>/edit', views.PersonalProfileInformation.as_view(), name='profile_edit'),
    path('profile/<int:id>', views.ProfileApplicant.as_view(), name='profile'),
    path('profile/busca-perfil', views.BuscaPerfil.as_view(), name='busca_perfil'),
    path('api/profile/<int:id>/competence', views.CompetenceAPI.as_view(), name='save_competence'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
