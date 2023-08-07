from django.urls import include, path
from company import views as views

urlpatterns = [
    path('company/<int:id>', views.CompanyProfile.as_view(), name='company_profile'),
]