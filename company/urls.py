from django.urls import include, path
from company import views as views

urlpatterns = [
    path('company/<int:id>', views.CompanyProfile.as_view(), name='company_profile'),
    path('company/<int:id>/edit', views.CompanyRegisterTemplateView.as_view(), name='company_edit'),
    path('api/company/<int:id>/edit', views.CompanyRegisterAPI.as_view(), name='company_api_edit'),
]