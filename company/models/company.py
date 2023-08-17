from django.contrib.auth import get_user_model
from django.db import models

from users.choices import STATES

User = get_user_model()


class Company(models.Model):
    name = models.CharField(
        max_length=80,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="Empresa",
    )
    cnpj = models.CharField(
        max_length=14, db_index=True, blank=True, null=True, verbose_name="CNPJ"
    )
    photo = models.ImageField(
        blank=True, null=True, upload_to='', verbose_name='Logo empresa'
    )
    about_us = models.CharField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name="Empresa",
    )
    business_area = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name="Areas de atuação",
    )
    state = models.CharField(max_length=200, verbose_name="Estado", choices=STATES)
    city = models.CharField(max_length=200, verbose_name="Cidade")

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return str(self.pk)

    def create_vacancy(self):
        return
    
    def create_company_profile(self, email):
        # TODO colocar try/except na view que chamar esse metodo django.db.utils.IntegrityError: UNIQUE constraint failed: auth_user.username
        user = User.objects.create_user(username=email, email=email, password=f'{self.name}1234')
        profile = user.profile
        profile.is_company = True
        profile.company = self
        profile.save()
    
    @property
    def get_url_photo(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "/static/images/company.png"
