# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

User = get_user_model()


def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, '')

def signup(request):
    if request.method == 'POST':
        post = request.POST
        email = post.get('email')
        password = post.get('password')
        users = User.objects.filter(username=email).first()

        if users:
            # TODO colocar um retorno para a mesma pagina
            return HttpResponse('E-mail já cadastrado')
        
        #TODO fazer verificação com a planilha da EY


        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        # TODO colocar o redirecionamento para continuar o cadastro
        return HttpResponse("Usuário cadastrado com sucesso")

    return render(request, 'users/signup.html')

def login_view(request):
    if request.method == 'POST':
        post = request.POST
        email = post.get('email')
        password = post.get('password')

        find_user = User.objects.filter(email=email).first()
        username = find_user.username if find_user else None

        user = authenticate(username=username, password=password)
        
        if user:
            # TODO colocar o redirecionamento para a pagina home após o login
            login(request, user)
            return HttpResponse("Autenticado")
        
        # TODO colocar um retorno para a mesma pagina para dar um retorno para o cliente
        return HttpResponse("E-mail ou senha inválidos")

    return render(request, 'users/login.html')


class BuscaPerfil(TemplateView):
    template_name = 'users/busca_perfil.html'
    