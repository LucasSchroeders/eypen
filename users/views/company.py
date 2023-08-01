from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import TemplateView

from users.models import Company


class CompanyProfile(TemplateView):
    template_name = 'users/company/company_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.filter(id=kwargs.get('id')).first()
        #TODO precisa enviar as vagas relacionadas a empresa

        return context
    

class BuscaCompany(TemplateView):
    template_name = 'users/company/busca_company.html'

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
