from django.shortcuts import render, redirect

from users.decorator import company_only


@company_only
def create_step(request, id, id_vacancy):
    return render(request, 'company/vagas/vaga_etapa_register.html')