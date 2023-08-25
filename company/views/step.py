from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from users.choices import  VULNERABILITIES_CHOICES
from users.decorator import company_only


@method_decorator(company_only, 'dispatch')
class StepTemplateView(TemplateView):
    template_name = 'company/vagas/etapa_register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vulnerabilities'] = VULNERABILITIES_CHOICES
        context['id_vacancy'] = kwargs.get('id_vacancy')
        context['id_company'] = kwargs.get('id')

        return context