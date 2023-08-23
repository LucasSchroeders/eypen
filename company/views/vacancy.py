from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views import View

from company.models import Company, Vacancy
from users.choices import STATES, JOB_MODALITY, SENIORITY_CHOICES, JOB_TYPE
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


@company_only
def create_vacancy(request, id):
    company = Company.objects.filter(id=id).first()

    if request.method == 'POST':
        post = request.POST
        
        vacancy_data = {
            'job_position': post.get('cargo'),
            'seniority': post.get('senioridade'),
            'job_modality': post.get('modalidade'),
            'job_type': post.get('job_type'),
            'state': post.get('state'),
            'city':  post.get('city'),
            'description': post.get('descricao-vaga'),
        }
        try:
            company.create_vacancy(**vacancy_data)
        except Exception as e:
            context = {
                'company': company,
                'states': STATES,
                'seniorities': SENIORITY_CHOICES,
                'modalities': JOB_MODALITY,
                'job_type': JOB_TYPE,
            }
            messages.add_message(
                request,
                messages.ERROR,
                f'ERRO! {str(e)}',
                extra_tags='Criação de vaga',
            )
            return render(request, 'company/vagas/vaga_register.html', context)
        
        messages.add_message(
            request,
            messages.SUCCESS,
            f'Vaga criada com sucesso!',
            extra_tags='Criação de vaga',
        )

        return redirect('company_profile', id=id)
    
    context = {
        'company': company,
        'states': STATES,
        'seniorities': SENIORITY_CHOICES,
        'modalities': JOB_MODALITY,
        'job_type': JOB_TYPE,
    }
    
    return render(request, 'company/vagas/vaga_register.html', context)


@company_only
def update_vacancy(request, id, id_vacancy):
    company = Company.objects.filter(id=id).first()

    if request.method == 'POST':
        post = request.POST
        
        vacancy = Vacancy.objects.filter(id=id_vacancy).first()

        vacancy.job_position = post.get('cargo')
        vacancy.seniority = post.get('senioridade')
        vacancy.job_modality = post.get('modalidade')
        vacancy.job_type = post.get('job_type')
        vacancy.state = post.get('state')
        vacancy.city = post.get('city')
        vacancy.description = post.get('descricao-vaga')
        vacancy.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            f'Vaga atualizada com sucesso!',
            extra_tags='Atualização de vaga',
        )
        return redirect('company_profile', id=id)

    
    context = {
        'company': company,
        'vacancy': company.vacancies.filter(id=id_vacancy).first(),
        'states': STATES,
        'seniorities': SENIORITY_CHOICES,
        'modalities': JOB_MODALITY,
        'job_type': JOB_TYPE,
    }
    
    return render(request, 'company/vagas/vaga_register.html', context)
    