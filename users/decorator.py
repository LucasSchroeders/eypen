from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


def company_only(function):
    def _inner(request, *args, **kwargs):
        user = request.user
        profile = user.profile

        if not user.is_authenticated:
            messages.add_message(
                request,
                messages.ERROR,
                'Você não está logado! Faça o login para acessar a página!',
                extra_tags='Autenticação',
            )
            return  HttpResponseRedirect(reverse('login'))
        elif user.is_authenticated and not profile.is_company:
            messages.add_message(
                request,
                messages.ERROR,
                'Você não tem permissão para acessar essa página!',
                extra_tags='Autorização',
            )
            return redirect('profile', id=profile.id)

        return function(request, *args, **kwargs)
    
    return _inner


def applicant_only(function):
    def _inner(request, *args, **kwargs):
        user = request.user
        profile = user.profile

        if not user.is_authenticated:
            messages.add_message(
                request,
                messages.ERROR,
                'Você não está logado! Faça o login para acessar a página!',
                extra_tags='Autenticação',
            )
            return  HttpResponseRedirect(reverse('login'))
        elif user.is_authenticated and not profile.is_applicant:
            messages.add_message(
                request,
                messages.ERROR,
                'Você não tem permissão para acessar essa página!',
                extra_tags='Autorização',
            )
            return redirect('company_profile', id=profile.company.id)

        return function(request, *args, **kwargs)
    
    return _inner
