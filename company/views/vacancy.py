from django.views.generic import TemplateView

from users.choices import STATES


class VacancyTemplateView(TemplateView):
    template_name = 'company/vaga_company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        profile = request.user.profile

        context['profile_user'] = profile

        return context


class VacancyRegisterTemplateView(TemplateView):
    template_name = 'company/vaga_register.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        
        context['states'] = STATES

        return context