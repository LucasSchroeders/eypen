from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import Company
from users.choices import ETHNICITY_CHOICES, GENDER_CHOICES, DISABLED_CHOICES, STATES, JOB_MODALITY, JOB_TYPE
from users.decorator import applicant_only
from users.models import Profile, Competence, Experience, AcademicFormation
from users.permission import AllowOnlyApplicant, AllowOnlyCompany
from users.utils import string_to_date

User = get_user_model()


# @method_decorator(applicant_only, 'dispatch')
# class PersonalProfileInformation(TemplateView):
#     template_name='users/profile/personalProfile.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user
#         self.request.session['edit'] = 'true'
#         context['profile'] = user.profile
#         context['genders'] = GENDER_CHOICES
#         context['disables'] = DISABLED_CHOICES
#         context['states'] = STATES
#         context['ethnicities'] = ETHNICITY_CHOICES
#         return context


@applicant_only
def personalProfileInformation(request, id):
    if request.method == 'POST':
        post = request.POST
        cpf = post.get('cpf').replace('.', '').replace('.', '').replace('-', '')
        rg = post.get('rg').replace('.', '').replace('.', '').replace('-', '')
        gender = post.get('gender')
        ethnicity = post.get('ethnicity')
        birthdate = post.get('birthdate')
        curriculum = request.FILES.get('curriculum')
        try:
            birthdate = string_to_date(birthdate) if birthdate else None
        except Exception as e:
            messages.add_message(
                request,
                messages.ERROR,
                f'ERRO! {str(e)}',
                extra_tags='Alteração de perfil',
            )
            return redirect('profile_edit', id=id)
        
        # TODO fazer com que vire 8bits
        photo = request.FILES.get('foto')
        state = post.get('state')
        city = post.get('city')
        is_disabled = post.get('is_disabled')
        disabled = post.get('disabled')

        profile = Profile.objects.filter(id=id).first()

        profile.cpf = cpf
        profile.rg = rg
        profile.gender = gender
        profile.ethnicity = ethnicity
        profile.birthdate = birthdate
        if photo:
            profile.photo = photo
        profile.state = state
        profile.city = city
        profile.is_disabled = is_disabled
        profile.disabled = disabled
        profile.curriculum = curriculum

        profile.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            'Perfil salvo com sucesso!',
            extra_tags='Perfil salvo',
        )
    
        return redirect('profile', id=profile.id)
    
    context = {
        'profile': request.user.profile,
        'genders': GENDER_CHOICES,
        'disables': DISABLED_CHOICES,
        'states': STATES,
        'ethnicities': ETHNICITY_CHOICES,
        'edit': True,
    }
    
    return render(request, 'users/profile/personalProfile.html', context)


@method_decorator(login_required, 'dispatch')
class ProfileApplicant(TemplateView):
    template_name = 'users/profile/applicant_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        is_same_person = True if profile.id == kwargs.get('id') else False

        context['profile_user'] = profile
        if not is_same_person:
            profile = Profile.objects.filter(id=kwargs.get('id')).first()

        last_experience = profile.experience.filter(is_working=True).order_by('ended_at').last()
        last_formation = profile.academic_formation.order_by('ended_at').last()

        context['last_experience'] = last_experience
        context['last_formation'] = last_formation
        context['competences'] = profile.competence.all()
        context['academic_educations'] = profile.academic_formation.all()
        context['experiences'] = profile.experience.all()
        context['profile'] = profile
        context['is_same_profile'] = is_same_person
        context['job_type'] = JOB_TYPE
        context['job_modality'] = JOB_MODALITY

        return context


@method_decorator(login_required, 'dispatch')
class BuscaPerfil(TemplateView):
    template_name = 'users/profile/busca_perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        profile = request.user.profile

        name = request.GET.get('name', request.session.get('name', None))
        request.session["name"] = name

        gender = request.GET.get('gender', request.session.get('gender', None))
        request.session["gender"] = gender

        disabled = request.GET.get('disabled', request.session.get('disabled', None))
        request.session["disabled"] = disabled

        state = request.GET.get('state', request.session.get('state', None))
        request.session["state"] = state

        city = request.GET.get('city', request.session.get('city', None))
        request.session["city"] = city

        data_query = {
            'is_applicant': True,
            'is_company': False,
        }

        if name:
            data_query['name__contains'] = name

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
        context['ethnicities'] = ETHNICITY_CHOICES
        context['page_range'] = page_range

        return context


@permission_classes((AllowOnlyApplicant,))
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


@permission_classes((AllowOnlyApplicant,))
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
    

@permission_classes((AllowOnlyApplicant,))
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


@permission_classes((AllowOnlyApplicant,))
class AppliedVacancies(TemplateView):
    template_name = 'users/profile/applied_vacancies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        profile = request.user.profile

        # vacancies = Vacancy.objects.filter(candidates=profile)
        id_list = []
        vacancies_step = profile.vacancies_step.all()
        for vacancy in vacancies_step:
            id_list.append(vacancy.id)

        vacancies_approved = profile.vacancies_approved.all()
        for vacancy in vacancies_approved:
            id_list.append(vacancy.id)

        vacancies = profile.vacancies.filter(~Q(pk__in=id_list))

        context['profile_user'] = profile
        context['vacancies'] = vacancies
        context['vacancies_step'] = vacancies_step
        context['vacancies_approved'] = vacancies_approved
        return context


@permission_classes((AllowOnlyCompany,))
class ProfileRecruiterAPIView(APIView):
    def get(self, request, id):
        profile = Profile.objects.filter(id=id).first()
        user = profile.user
        context = {
            'user': {
                'id': profile.id,
                'name': user.first_name,
                'surname': user.last_name,
                'email': user.email,
                'password': user.password,
            }
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def post(self, request, id):
        data = request.data
        email = data.get('email')
        name = data.get('name')
        surname = data.get('surname')
        password = data.get('password')

        users = User.objects.filter(username=email).first()

        if users:
            return Response({'detail': 'Email já está cadastrado!', 'type': 'error'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        company = Company.objects.filter(id=id).first()
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.last_name = surname
            user.save()
            profile = user.profile
            profile.name = ' '.join([name, surname])
            profile.company = company
            profile.is_company = True
            profile.save()
            context = {
                'user': {
                    'id': profile.id,
                    'email': email,
                    'name': profile.name,
                }, 
                'detail': 'Administrador criado com sucesso!',
                'type': 'success',
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível ciar o perfil de administrador! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                    'type': 'error',
                }
            )

    def put(self, request, id):
        data = request.data
        email = data.get('email')
        new_email = data.get('new_email')
        name = data.get('name')
        surname = data.get('surname')
        password = data.get('password')
        users = User.objects.filter(username=new_email).first()

        if not email == new_email and users:
            return Response({'detail': 'Email já está cadastrado!', 'type': 'error'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        try:
            profile = Profile.objects.filter(id=id).first()
            profile.name = ' '.join([name, surname])
            profile.save()
            user = profile.user
            user.email = new_email
            user.username = new_email
            user.set_password(password)
            user.first_name = name
            user.last_name = surname
            user.save()
            context = {
                    'user': {
                        'id': profile.id, 
                        'email': new_email,
                        'name': profile.name,
                    }, 
                    'detail': 'Administrador atualizado com sucesso!',
                    'type': 'success',
                }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível atualizar o perfil de administrador! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                    'type': 'error',
                }
            )

    def delete(self, request, id):
        profile = Profile.objects.filter(id=id).first()
        user = profile.user

        try:
            user.delete()
            return Response({'detail': 'Perfil de administrador excluído com sucesso!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível excluir a etapa! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
