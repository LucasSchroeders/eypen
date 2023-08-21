from django.urls import include, path
from company import views as views

urlpatterns = [
    path('company/<int:id>', views.CompanyProfile.as_view(), name='company_profile'),
    path('company/<int:id>/edit', views.companyRegister, name='company_edit'),
    path('company/vagas/selective-process', views.VacancySelectiveProcessTemplateView.as_view(), name='vagas_processo_seletivo'), #TODO ao fazer o back, colocar os ids das vaga e empresa
]