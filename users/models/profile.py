from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.choices import STATES
from users.models import Competence

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        "auth.user",
        related_name="profile",
        verbose_name="Usuário",
        on_delete=models.CASCADE,
    )
    full_name = models.CharField(
        max_length=80,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="Nome Completo",
    )
    cpf = models.CharField(
        max_length=14, db_index=True, blank=True, null=True, verbose_name="CPF"
    )
    cpf_hashed = models.CharField(
        max_length=200, db_index=True, blank=True, null=True, verbose_name="CPF Hash"
    )
    rg = models.CharField(max_length=9, blank=True, null=True, verbose_name="RG")
    gender = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Gênero"
    )
    ethnicity = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Etnia"
    )
    birthdate = models.DateField(blank=True, null=True, verbose_name="Data Nascimento")
    photo = models.FileField(
        blank=True, null=True, verbose_name='Foto de Perfil'
    )
    state = models.CharField(max_length=200, verbose_name="Estado", choices=STATES)
    city = models.CharField(max_length=200, verbose_name="Cidade")
    is_disabled = models.BooleanField(default=False, db_index=True, verbose_name='Possui deficiência')
    disabled = models.CharField(max_length=30, blank=True, null=True, verbose_name='Deficiência')
    is_internal = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
        indexes = [
            models.Index(fields=['full_name']),
            models.Index(fields=['cpf', 'cpf_hashed']),
            models.Index(fields=['is_disabled']),
        ]

    def __str__(self):
        return str(self.pk)
    
    def create_competence(self, context):
        academic_formation = self.academic_formation.filter(id=context.get('academic_formation_id'))
        experience = self.experience.filter(id=context.get('experience_id'))

        competence_data = {
            'competence_name': context.get('competence_name'),
            'academic_formation': academic_formation,
            'experience': experience,
        }

        self.competence.create(**competence_data)
        return True


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, is_internal=False)
    instance.profile.save()
