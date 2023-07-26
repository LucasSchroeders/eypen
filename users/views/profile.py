from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.utils import string_to_date
from users.models import Profile, Competence, Experience, AcademicFormation


class PersonalProfileInformation(TemplateView):
    template_name='users/profile/personalProfile.html'

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
    template_name = 'users/company/company_profile.html'


class ProfileApplicant(TemplateView):
    template_name = 'users/profile/applicant_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_same_person = True if user.profile.id == kwargs.get('id') else False

        context['profile_user'] = user.profile
        context['competences'] = user.profile.competence.all()
        context['academic_educations'] = user.profile.academic_formation.all()
        context['experiences'] = user.profile.experience.all()
        context['profile'] = (
            user.profile
            if is_same_person 
            else Profile.objects.filter(id=kwargs.get('id'))
        )
        context['is_same_profile'] = is_same_person

        return context


class BuscaPerfil(TemplateView):
    template_name = 'users/profile/busca_perfil.html'


class CompetenceAPI(APIView):
    def get(self, request, id):
        competence = Competence.objects.filter(profile__id=request.user.profile.id, id=id).first()
        a = competence.to_dict()
        return Response({'detail': competence.to_dict()}, status=status.HTTP_200_OK)
    
    def post(self, request, id):
        profile = Profile.objects.filter(id=id).first()

        data = request.data

        context = {
            'competence': data.get('competence'),
            'experience_list': data.get('experiences'),
            'academic_list': data.get('academic_traning'),
        }

        try:
            profile.create_competence(context)
            return Response({'detail': 'Competência salva com sucesso!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível salvar a competência! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
        
    def put(self, request, id):
        competence = Competence.objects.filter(profile__id=request.user.profile.id, id=id).first()

        data = request.data

        context = {
            'competence_name': data.get('competence'),
            'experience_list': data.get('experiences'),
            'academic_list': data.get('academic_traning'),
        }

        competence.update(context)

        return Response({'detail': 'Competência atualizada com sucesso!'}, status=status.HTTP_200_OK)
        
    def delete(self, request, id):
        competence = Competence.objects.filter(profile__id=request.user.profile.id, id=id)

        try:
            competence.delete()
            return Response({'detail': 'Competência excluída com sucesso!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível excluir a competência! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )

