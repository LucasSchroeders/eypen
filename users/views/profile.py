from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.choices import GENDER_CHOICES, DISABLED_CHOICES, STATES
from users.models import Profile, Competence, Experience, AcademicFormation
from users.utils import string_to_date


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
        profile = self.request.user.profile
        is_same_person = True if profile.id == kwargs.get('id') else False

        context['profile_user'] = profile
        if not is_same_person:
            profile = Profile.objects.filter(id=kwargs.get('id')).first()

        context['competences'] = profile.competence.all()
        context['academic_educations'] = profile.academic_formation.all()
        context['experiences'] = profile.experience.all()
        context['profile'] = profile
        context['is_same_profile'] = is_same_person

        return context


class BuscaPerfil(TemplateView):
    template_name = 'users/profile/busca_perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        profile = request.user.profile

        full_name = request.GET.get('full_name', request.session.get('full_name', None))
        request.session["full_name"] = full_name

        gender = request.GET.get('gender', request.session.get('gender', None))
        request.session["gender"] = gender

        disabled = request.GET.get('disabled', request.session.get('disabled', None))
        request.session["disabled"] = disabled

        state = request.GET.get('state', request.session.get('state', None))
        request.session["state"] = state

        city = request.GET.get('city', request.session.get('city', None))
        request.session["city"] = city

        data_query = {}

        if full_name:
            data_query['full_name__contains'] = full_name

        if gender:
            data_query['gender'] = gender

        if disabled:
            data_query['disabled'] = disabled

        if state:
            data_query['state'] = state

        if city:
            data_query['city'] = city

        #TODO colocar o is_applicant = True no filter
        profile_list = Profile.objects.filter(**data_query).exclude(id=profile.id)

        page = request.GET.get('page', 1)

        paginator = Paginator(profile_list, settings.PAGINATION_PAGE_DEFAULT)

        try:
            profile_pag = paginator.page(page)
        except PageNotAnInteger:
            profile_pag = paginator.page(1)
        except EmptyPage:
            profile_pag = paginator.page(paginator.num_pages)

        index = profile_pag.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range)[start_index:end_index]
            
        context['profile_user'] = profile
        context['experience'] = profile.experience.filter(is_working=True).first()
        context['profile_list'] = profile_pag
        context['genders'] = GENDER_CHOICES
        context['disables'] = DISABLED_CHOICES
        context['states'] = STATES
        context['page_range'] = page_range

        return context

class CompetenceAPI(APIView):
    def get(self, request, id):
        competence = Competence.objects.filter(profile__id=request.user.profile.id, id=id).first()
        
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
            competence = profile.create_competence(context)

            return Response({'detail': 'Competência salva com sucesso!', 'competence': competence, 'status': status.HTTP_200_OK})
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

        competence_updated = competence.update(context)

        return Response({'detail': 'Competência atualizada com sucesso!', 'competence': competence_updated}, status=status.HTTP_200_OK)
        
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


class ExperienceAPI(APIView):
    def get(self, request, id):
        experience = Experience.objects.filter(profile__id=request.user.profile.id, id=id).first()

        return Response({'detail': experience.to_dict()}, status=status.HTTP_200_OK)

    def post(self, request, id):
        profile = Profile.objects.filter(id=id).first()

        data = request.data

        context = {
            'position': data.get('position'),
            'job_type': data.get('job_type'),
            'job_modality': data.get('job_modality'),
            'is_working': data.get('is_working'),
            'company': data.get('company'),
            'business_area': data.get('business_area'),
            'started_at': data.get('started_at'),
            'ended_at': data.get('ended_at'),
        }

        
        try:            
            experience = profile.create_experience(context)
            return Response({'detail': 'Experiência salva com sucesso!', 'experience': experience}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível salvar a experiência! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
        # TODO fazer retorno com mensagem

    def put(self, request, id):
        experience = Experience.objects.filter(profile__id=request.user.profile.id, id=id).first()

        data = request.data

        context = {
            'position': data.get('position'),
            'job_type': data.get('job_type'),
            'job_modality': data.get('job_modality'),
            'is_working': data.get('is_working'),
            'company': data.get('company'),
            'business_area': data.get('business_area'),
            'started_at': data.get('started_at'),
            'ended_at': data.get('ended_at'),
        }

        experience_updated = experience.update(context)

        return Response({'detail': 'Experiência atualizada com sucesso!', 'experience': experience_updated}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        experience = Experience.objects.filter(profile__id=request.user.profile.id, id=id)

        try:
            experience.delete()
            return Response({'detail': 'Experiência excluída com sucesso!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível excluir a experiência! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
    

class AcademicFormationAPI(APIView):
    def get(self, request, id):
        academic = AcademicFormation.objects.filter(profile__id=request.user.profile.id, id=id).first()

        return Response({'detail': academic.to_dict()}, status=status.HTTP_200_OK)
    
    def post(self, request, id):
        profile = Profile.objects.filter(id=id).first()

        data = request.data

        context = {
            'educational_institution': data.get('educational_institution'),
            'course': data.get('course'),
            'knowledge_area': data.get('knowledge_area'),
            'started_at': data.get('started_at'),
            'ended_at': data.get('ended_at'),
        }

        try:            
            academic = profile.create_academic_formation(context) 
            return Response({'detail': 'Formação Acadêmica salva com sucesso!', 'academic': academic}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível salvar a formação acadêmica! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
        
    def put(self, request, id):
        academic = AcademicFormation.objects.filter(profile__id=request.user.profile.id, id=id).first()

        data = request.data
        context = {
            'educational_institution': data.get('educational_institution'),
            'course': data.get('course'),
            'knowledge_area': data.get('knowledge_area'),
            'started_at': data.get('started_at'),
            'ended_at': data.get('ended_at'),
        }
            
        academic_updated = academic.update(context)

        return Response({'detail': 'Formação Acadêmica atualizada com sucesso!', 'academic': academic_updated}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        academic = AcademicFormation.objects.filter(profile__id=request.user.profile.id, id=id)

        try:
            academic.delete()
            return Response({'detail': 'Formação acadêmica excluída com sucesso!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível excluir a formação acadêmica! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
