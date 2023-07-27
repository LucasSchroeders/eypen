import re

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

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
        return redirect('profile', id=request.user.profile.id)
    
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
            
            return redirect(f'profile', id=user.profile.id)
        
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
        photo = request.FILES.get('photo')

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

        profile.save()
        
        return redirect('profile', id=profile.id)
    
    return render(request, 'users/profile/personalProfile.html')
