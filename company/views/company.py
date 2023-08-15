import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import Company
from users.choices import STATES
from users.decorator import company_only, applicant_only
from users.permission import AllowOnlyCompany


@method_decorator(login_required, 'dispatch')
class CompanyProfile(TemplateView):
    template_name = 'company/company_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.filter(id=kwargs.get('id')).first()
        context['company'] = company
        context['profile_user'] = self.request.user.profile
        #TODO precisa enviar as vagas relacionadas a empresa

        return context
    

@method_decorator(applicant_only, 'dispatch')
class BuscaCompany(TemplateView):
    template_name = 'company/busca_company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        profile = request.user.profile

        company_name = request.GET.get('company', request.session.get('company', None))
        request.session["company"] = company_name

        business_area = request.GET.get('business_area', request.session.get('business_area', None))
        request.session["business_area"] = business_area

        data_query = {}

        if company_name:
            data_query['name__contains'] = company_name

        if business_area:
            data_query['business_area'] = business_area

        company_list = Company.objects.filter(**data_query)

        page = request.GET.get('page', 1)

        paginator = Paginator(company_list, settings.PAGINATION_PAGE_DEFAULT)

        try:
            company_pag = paginator.page(page)
        except PageNotAnInteger:
            company_pag = paginator.page(1)
        except EmptyPage:
            company_pag = paginator.page(paginator.num_pages)

        index = company_pag.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range)[start_index:end_index]

        context['profile_user'] = profile
        context['company_list'] = company_pag
        context['page_range'] = page_range

        return context


# @method_decorator(company_only, 'dispatch')
# class CompanyRegisterTemplateView(TemplateView):
#     template_name = 'company/company_register.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         company = Company.objects.filter(id=kwargs.get('id')).first()
#         jsonDec = json.decoder.JSONDecoder()
#         business_areas = jsonDec.decode(company.business_areas)

#         self.request.session['edit'] = 'true'

#         context['company'] = company
#         context['business_areas'] = business_areas
#         context['states'] = STATES

#         return context

@company_only
def companyRegister(request, id):
    if request.method == 'POST':
        post = request.POST
        name = post.get('name')
        cnpj = post.get('cnpj').replace('.', '').replace('.', '').replace('/', '').replace('-', '')
        photo = request.FILES.get('foto')
        about_us = post.get('about-us')
        #TODO descomentar quando colocar as choices
        # areas_list = []
        # for k, v in BUSINESS_AREAS_CHOICES:
        #     if post.get(k):
        #         areas_list.append(k)
        # business_areas = json.dumps(areas_list)
        business_areas = json.dumps(business_areas)
        state = post.get('state')
        city = post.get('city')

        company = Company.objects.filter(id=id).first()

        company.name = name
        company.cnpj = cnpj
        if photo:
            company.photo = photo
        company.about_us = about_us
        company.business_areas = business_areas
        company.state = state
        company.city = city

        company.save()
    
        messages.add_message(
            request,
            messages.SUCCESS,
            'Empresa atualizada com sucesso!',
            extra_tags='Perfil salvo',
        )

        return redirect('company_profile', id=company.id)

    company = request.user.profile.company

    jsonDec = json.decoder.JSONDecoder()
    business_areas = jsonDec.decode(company.business_areas)

    context = {
        'company': company,
        'business_areas': business_areas,
        'states': STATES
    }

    return render(request, 'company/company_register.html', context)

# @permission_classes((AllowOnlyCompany,))
# class CompanyRegisterAPI(APIView):
#     def post(self, request, id):
#         data = request.data
#         name = data.get('name')
#         cnpj = data.get('cnpj')
#         photo = request.FILES.get('foto')
#         about_us = data.get('about_us')
#         business_areas = data.get('business_areas')
#         business_areas = json.dumps(business_areas)
#         state = data.get('state')
#         city = data.get('city')

#         company = Company.objects.filter(id=id).first()

#         company.name = name
#         company.cnpj = cnpj
#         company.photo = photo
#         company.about_us = about_us
#         company.business_areas = business_areas
#         company.state = state
#         company.city = city

#         company.save()
        
#         return Response(
#             {
#                 "detail": "Empresa atualizada com sucesso!",
#                 "status": status.HTTP_200_OK,
#             }
#         )
