from django.db import models
from users.choices import STATES


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
