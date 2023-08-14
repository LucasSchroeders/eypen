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
from users.choices import GENDER_CHOICES, DISABLED_CHOICES, STATES, ETHNICITY_CHOICES
from users.utils import string_to_date

User = get_user_model()


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        post = request.POST
        email = post.get('email')
        password = post.get('password')
        full_name = post.get('name')
        full_name = full_name.strip() if full_name else full_name
        users = User.objects.filter(username=email).first()

        if users:
            # TODO colocar um retorno para a mesma pagina
            return HttpResponse('E-mail já cadastrado')
        
        #TODO fazer verificação com a planilha da EY

        #TODO fazer validação de senhas

        user = User.objects.create_user(username=email, email=email, password=password)
        full_name = ' '.join(
            re.sub(r'[^\w ]+', '', full_name.replace('&#x27;', '')).split()
        )
        user.first_name = full_name.split()[0].capitalize()[:30]
        user.last_name = ' '.join(full_name.split()[1:])
        user.save()
        
        user = authenticate(username=email, password=password)
        login(request, user)
        return redirect('signup2')

    return render(request, 'users/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.profile.is_applicant:
            return redirect('profile', id=request.user.profile.id)
        # TODO return para a pagina de entrada da empresa
    
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
                # TODO return para a pagina de entrada da empresa
                company = user.profile.company
                return redirect('company_profile', id=company.id)
            
            return redirect('profile', id=user.profile.id)
        
        # TODO colocar um retorno para a mesma pagina para dar um retorno para o cliente
        return HttpResponse("E-mail ou senha inválidos")

    return render(request, 'users/login.html')


@login_required
def signup2(request):
    if request.method == 'POST':
        post = request.POST
        user = request.user

        cpf = post.get('cpf')
        rg = post.get('rg')
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
        
        profile.full_name = ' '.join([user.first_name, user.last_name])
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
        
        return redirect('profile', id=profile.id)
    
    context = {
        'genders': GENDER_CHOICES,
        'disables': DISABLED_CHOICES,
        'states': STATES,
        'ethnicities': ETHNICITY_CHOICES,
    }
    
    return render(request, 'users/profile/personalProfile.html', context)


def signup_company(request):
    request.session['edit'] = 'false'

    if request.method == 'POST':

        data = request.body

        if isinstance(data, bytes):
            data = literal_eval(data.decode('utf8'))
        name = data.get('name')
        cnpj = data.get('cnpj')

        company = Company.objects.filter(cnpj=cnpj).first()
        if company:
            return Response(
                {'detail': 'Já existe uma empresa cadastrada com esse CNPJ!', 'status': status.HTTP_400_BAD_REQUEST}
            )
        
        photo = request.FILES.get('photo')
        business_areas = data.get('business_area')
        business_areas = json.dumps(business_areas)
        state = data.get('state')
        city = data.get('city')

        data_company = {
            'name': name,
            'cnpj': cnpj,
            'photo': photo,
            'business_areas': business_areas,
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
    
    return render(request, 'company/company_register.html', {'states': STATES})
