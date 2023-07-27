from django.urls import path
from users import views as views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastro', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', auth_views.LogoutView.as_view, name="logout"),
    path('profile/company', views.ProfileCompany.as_view(), name='profile_company'),
    path('cadastro/2', views.signup2, name='signup2'),
    path('profile/<int:id>/edit', views.PersonalProfileInformation.as_view(), name='profile_edit'),
    path('profile/<int:id>', views.ProfileApplicant.as_view(), name='profile'),
    path('profile/busca-perfil', views.BuscaPerfil.as_view(), name='busca_perfil'),
    path('api/profile/<int:id>/competence', views.CompetenceAPI.as_view(), name='save_competence'),
    path('api/profile/<int:id>/experience', views.ExperienceAPI.as_view(), name='save_experience'),
    path('api/profile/<int:id>/academic-formation', views.AcademicFormationAPI.as_view(), name='save_academic_formation'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
