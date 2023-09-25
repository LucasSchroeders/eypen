from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.decorators import permission_classes 
from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import Step, Vacancy
from users.choices import  VULNERABILITIES_CHOICES
from users.decorator import company_only
from users.permission import AllowOnlyCompany


@method_decorator(company_only, 'dispatch')
class StepTemplateView(TemplateView):
    template_name = 'company/vagas/etapa_register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_vacancy = kwargs.get('id_vacancy')
        vacancy = Vacancy.objects.filter(id=id_vacancy).first()
        context['vulnerabilities'] = VULNERABILITIES_CHOICES
        context['id_vacancy'] = id_vacancy
        context['id_company'] = kwargs.get('id')
        context['steps'] = vacancy.steps.all()

        return context
    

@permission_classes((AllowOnlyCompany,))
class StepAPIView(APIView):
    def get(self, request, id):
        step = Step.objects.filter(id=id).first()
        return Response({'detail': step.to_dict()}, status=status.HTTP_200_OK)
    
    def post(self, request, id):
        vacancy = Vacancy.objects.filter(id=id).first()
        data = request.data

        context = {
            'step': data.get('step'),
            'title': data.get('title'),
            'step_modality': data.get('step_modality'),
            'step_type': data.get('step_type'),
            'description': data.get('description'),
        }

        try:            
            step = vacancy.create_step(**context)
            return Response({'detail': 'Etapa criada com sucesso!', 'step': step}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível ciar a etapa! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
    
    def put(self, request, id):
        step = Step.objects.filter(id=id).first()

        data = request.data

        context = {
            'step': data.get('step'),
            'title': data.get('title'),
            'step_modality': data.get('step_modality'),
            'step_type': data.get('step_type'),
            'description': data.get('description'),
        }

        step = step.update(context)

        return Response({'detail': 'Etapa atualizada com sucesso!', 'step': step}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        step = Step.objects.filter(id=id).first()

        try:
            step.delete()
            return Response({'detail': 'Etapa excluída com sucesso!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    "detail": f"Não foi possível excluir a etapa! {e}",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
