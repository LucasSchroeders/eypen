from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from users.choices import STATES
from users.decorator import company_only


@method_decorator(login_required, 'dispatch')
class VacancyTemplateView(TemplateView):
    template_name = 'company/vagas/vaga_company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        profile = request.user.profile

        context['profile_user'] = profile

        return context


@method_decorator(company_only, 'dispatch')
class VacancyRegisterTemplateView(TemplateView):
    template_name = 'company/vagas/vaga_register.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        
        context['states'] = STATES

        return context


@method_decorator(company_only, 'dispatch')
class VacancySelectiveProcessTemplateView(TemplateView):
    template_name = 'company/vagas/vagas_approve.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.request.user.profile

        return context
