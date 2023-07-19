from django.views.generic import TemplateView
from django.shortcuts import render 
from rest_framework.views import APIView

from users.utils import string_to_date
from users.models import Profile


class PersonalProfileInformation(TemplateView):
    template_name='users/personalProfile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_authenticated = self.request.user.is_authenticated
        context['profile'] = user.profile if is_authenticated else None
        return context


class PersonalProfileInformationAPI(APIView):
    def post(self, request):
        post = request.POST
        full_name = post.get('full_name')
        full_name = full_name.strip()
        cpf = post.get('cpf')
        rg = post.get('rg')
        gender = post.get('gender')
        ethnicity = post.get('ethnicity')
        birthdate = post.get('birthdate')
        try:
            birthdate = string_to_date(birthdate) if birthdate else None
        except Exception:
            # TODO fazer retorno com mensagem
            return
        # TODO fazer com que vire 8bits
        photo = post.get('photo')
        state = post.get('state')
        city = post.get('city')
        
        return


class ProfileCompany(TemplateView):
    template_name = 'users/company_profile.html'


class BuscaPerfil(TemplateView):
    template_name = 'users/busca_perfil.html'
