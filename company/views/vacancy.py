from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from company.models import Company, Vacancy
from users.choices import (
    STATES,
    SENIORITY_CHOICES,
    JOB_MODALITY,
    JOB_TYPE,
    BUSINESS_AREAS_CHOICES,
    VULNERABILITIES_CHOICES,
)
from users.decorator import company_only, applicant_only


@method_decorator(login_required, 'dispatch')
class VacancyTemplateView(TemplateView):
    template_name = 'company/vagas/vaga_company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        profile = request.user.profile
        id_company = kwargs.get('id')
        id_vacancy = kwargs.get('id_vacancy')
        vacancy = Vacancy.objects.filter(id=id_vacancy).first()

        context['profile_user'] = profile
        context['id_company'] = id_company
        context['vacancy'] = vacancy

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
            vacancy = company.create_vacancy(**vacancy_data)
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

        return redirect('registrar_etapa', id=id, id_vacancy=vacancy.id)
    
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


@method_decorator(applicant_only, 'dispatch')
class BuscaVacancy(TemplateView):
    template_name = 'company/vagas/busca_vaga.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        profile = request.user.profile

        company_name = request.GET.get('company', request.session.get('company', None))
        request.session["company"] = company_name

        vacancy = request.GET.get('vacancy', request.session.get('vacancy', None))
        request.session["vacancy"] = vacancy

        business_area = request.GET.get('business_area', request.session.get('business_area', None))
        request.session["business_area"] = business_area

        vulnerability = request.GET.get('vulnerability', request.session.get('vulnerability', None))
        request.session["vulnerability"] = vulnerability

        seniority = request.GET.get('seniority', request.session.get('seniority', None))
        request.session["seniority"] = seniority

        job_modality = request.GET.get('job_modality', request.session.get('job_modality', None))
        request.session["job_modality"] = job_modality

        job_type = request.GET.get('job_type', request.session.get('job_type', None))
        request.session["job_type"] = job_type

        data_query = {}

        if company_name:
            data_query['company__name__contains'] = company_name

        if vacancy:
            data_query['job_position__contains'] = vacancy

        if business_area:
            data_query['business_area'] = business_area

        if vulnerability:
            data_query['vulnerability'] = vulnerability

        if seniority:
            data_query['seniority'] = seniority

        if job_modality:
            data_query['job_modality'] = job_modality

        if job_type:
            data_query['job_type'] = job_type

        vacancy_list = Vacancy.objects.filter(**data_query).order_by('id')

        page = request.GET.get('page', 1)

        paginator = Paginator(vacancy_list, settings.PAGINATION_PAGE_DEFAULT)

        try:
            vacancy_pag = paginator.page(page)
        except PageNotAnInteger:
            vacancy_pag = paginator.page(1)
        except EmptyPage:
            vacancy_pag = paginator.page(paginator.num_pages)

        index = vacancy_pag.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range)[start_index:end_index]

        context['profile_user'] = profile
        context['vacancy_list'] = vacancy_pag
        context['page_range'] = page_range
        context['business_areas'] = BUSINESS_AREAS_CHOICES
        context['seniorities'] = SENIORITY_CHOICES
        context['job_modality'] = JOB_MODALITY
        context['job_type'] = JOB_TYPE
        context['vulnerabilities'] = VULNERABILITIES_CHOICES

        return context
