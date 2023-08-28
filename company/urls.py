from django.urls import path
from company import views as views

urlpatterns = [
    path('company/<int:id>', views.CompanyProfile.as_view(), name='company_profile'),
    path('company/<int:id>/edit', views.companyRegister, name='company_edit'),
    path('company/<int:id>/vagas/<int:id_vacancy>', views.VacancyTemplateView.as_view(), name='exibir_vagas'), #TODO ao fazer o back, colocar os ids das vaga e empresa
    path('company/<int:id>/vagas/cadastro', views.create_vacancy, name='registrar_vagas'),
    path('company/<int:id>/vagas/<int:id_vacancy>/edit', views.update_vacancy, name='editar_vagas'),
    path('company/<int:id>/vagas/<int:id_vacancy>/step', views.StepTemplateView.as_view(), name='registrar_etapa'),
    path('api/vagas/<int:id>/step', views.StepAPIView.as_view(), name='save_step'),
    path('company/vagas/selective-process', views.VacancySelectiveProcessTemplateView.as_view(), name='vagas_processo_seletivo'), #TODO ao fazer o back, colocar os ids das vaga e empresa
    path('company/busca-vagas', views.BuscaVacancy.as_view(), name='busca_vagas'),
]