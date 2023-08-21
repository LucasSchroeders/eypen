from django.urls import path
from users import views as views
from company import views as views_company
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/<int:id>/edit', views.personalProfileInformation, name='profile_edit'),
    # path('api/profile/<int:id>/edit', views.personalInformationAPI, name='profile_api_edit'),
    path('profile/<int:id>', views.ProfileApplicant.as_view(), name='profile'),
    path('profile/busca-perfil', views.BuscaPerfil.as_view(), name='busca_perfil'),
    path('api/profile/<int:id>/competence', views.CompetenceAPI.as_view(), name='save_competence'),
    path('api/profile/<int:id>/experience', views.ExperienceAPI.as_view(), name='save_experience'),
    path('api/profile/<int:id>/academic-formation', views.AcademicFormationAPI.as_view(), name='save_academic_formation'),
    path('profile/busca-empresa', views_company.BuscaCompany.as_view(), name='busca_empresa')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
