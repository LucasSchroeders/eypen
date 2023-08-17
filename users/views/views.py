import json
import re

from ast import literal_eval
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response

from company.models import Company
from users.choices import GENDER_CHOICES, DISABLED_CHOICES, STATES, ETHNICITY_CHOICES, BUSINESS_AREAS_CHOICES
from users.utils import string_to_date

User = get_user_model()


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        post = request.POST
        email = post.get('email')
        password = post.get('password')
        name = post.get('name')
        name = name.strip() if name else name
        users = User.objects.filter(username=email).first()

        if users:
            # TODO colocar um retorno para a mesma pagina
            return HttpResponse('E-mail já cadastrado')
        
        #TODO fazer verificação com a planilha da EY

        #TODO fazer validação de senhas

        user = User.objects.create_user(username=email, email=email, password=password)
        name = ' '.join(
            re.sub(r'[^\w ]+', '', name.replace('&#x27;', '')).split()
        )
        user.first_name = name.split()[0].capitalize()[:30]
        user.last_name = ' '.join(name.split()[1:])
        user.save()
        
        user = authenticate(username=email, password=password)
        login(request, user)
        return redirect('signup2')

    return render(request, 'users/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.profile.is_applicant:
            return redirect('profile', id=request.user.profile.id)
        elif request.user.profile.is_company:
            return redirect('company_profile', id = request.user.profile.company.id)
    
    if request.method == 'POST':
        post = request.POST
        email = post.get('email')
        password = post.get('password')

        find_user = User.objects.filter(email=email).first()
        username = find_user.username if find_user else None

        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)

            if not user.profile:
                return redirect('signup2')
            
            if user.profile.is_company:
                return redirect('company_profile', id=user.profile.company.id)
            
            return redirect('profile', id=user.profile.id)
        
        # TODO colocar um retorno para a mesma pagina para dar um retorno para o cliente
        return HttpResponse("E-mail ou senha inválidos")

    return render(request, 'users/login.html')


@login_required
def signup2(request):
    if request.method == 'POST':
        post = request.POST
        user = request.user

        cpf = post.get('cpf').replace('.', '').replace('.', '').replace('-', '')
        rg = post.get('rg').replace('.', '').replace('.', '').replace('-', '')
        birthdate = post.get('birthdate')
        gender = post.get('gender')
        ethnicity = post.get('ethnicity')
        state = post.get('state')
        city = post.get('city')
        is_disabled = post.get('is_disabled', False)
        disabled = post.get('disabled', '')
        photo = request.FILES.get('foto')

        birthdate = string_to_date(birthdate) if birthdate else None

        profile = user.profile
        
        profile.name = ' '.join([user.first_name, user.last_name])
        profile.cpf = cpf
        profile.rg = rg
        profile.birthdate = birthdate
        profile.gender = gender
        profile.ethnicity = ethnicity
        profile.state = state
        profile.city = city
        profile.is_disabled = is_disabled
        profile.disabled = disabled
        profile.photo = photo
        profile.is_applicant = True

        profile.save()
        
        messages.add_message(
            request,
            messages.SUCCESS,
            'Perfil criado com sucesso!',
            extra_tags='Perfil criado',
        )

        return redirect('profile', id=profile.id)
    
    context = {
        'genders': GENDER_CHOICES,
        'disables': DISABLED_CHOICES,
        'states': STATES,
        'ethnicities': ETHNICITY_CHOICES,
    }
    
    return render(request, 'users/profile/personalProfile.html', context)


def signup_company(request):
    if request.method == 'POST':

        post = request.POST

        name = post.get('name')
        cnpj = post.get('cnpj').replace('.', '').replace('.', '').replace('/', '').replace('-', '')

        company = Company.objects.filter(cnpj=cnpj).first()
        if company:
            messages.add_message(
            request,
            messages.ERROR,
            'Já existe uma empresa cadastrada com esse CNPJ!',
            extra_tags='Criação de Empresa',
        )
            return render(request, 'company/company_register.html', {'states': STATES})
        
        photo = request.FILES.get('foto')
        business_area = post.get('business_area')
        state = post.get('state')
        city = post.get('city')

        data_company = {
            'name': name,
            'cnpj': cnpj,
            'photo': photo,
            'business_area': business_area,
            'city': city,
            'state': state,
        }

        company = Company.objects.create(**data_company)

        messages.add_message(
            request,
            messages.SUCCESS,
            'Empresa criada com sucesso!',
            extra_tags='Empresa criada',
        )
        
        return redirect('company_profile', id=company.id)
    
    return render(request, 'company/company_register.html', {'states': STATES, 'business_areas': BUSINESS_AREAS_CHOICES})
