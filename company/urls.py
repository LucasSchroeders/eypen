from django.urls import path
from company import views as views

urlpatterns = [
    path('company/<int:id>', views.CompanyProfile.as_view(), name='company_profile'),
    path('company/<int:id>/edit', views.companyRegister, name='company_edit'),
    path('company/<int:id>/vagas/<int:id_vacancy>', views.VacancyTemplateView.as_view(), name='exibir_vagas'),
    path('company/<int:id>/vagas/cadastro', views.create_vacancy, name='registrar_vagas'),
    path('company/<int:id>/vagas/<int:id_vacancy>/edit', views.update_vacancy, name='editar_vagas'),
    path('company/<int:id>/vagas/<int:id_vacancy>/step', views.StepTemplateView.as_view(), name='registrar_etapa'),
    path('api/vagas/<int:id>/step', views.StepAPIView.as_view(), name='save_step'),
    path('company/<int:id>/vagas/<int:id_vacancy>/selective-process', views.VacancySelectiveProcessTemplateView.as_view(), name='vagas_processo_seletivo'),
    path('company/<int:id>/vagas/<int:id_vacancy>/candidates', views.CandidatesVacancy.as_view(), name='candidatos_vagas'),
    path('company/busca-vagas', views.BuscaVacancy.as_view(), name='busca_vagas'),
    path('company/vagas/<int:id>/update', views.vacancy_update_view, name='atualizar_vaga'),
    path('api/vagas/<int:id>/selective-process', views.UpdateSelectiveProcess.as_view(), name='atualizar_processo_seletivo'),
    path('company/<int:id>/cadastro-admin', views.ProfileCompanyRegister.as_view(), name='cadastrar_admin'),
]