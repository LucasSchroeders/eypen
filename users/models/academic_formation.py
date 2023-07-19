from django.db import models


class AcademicFormation(models.Model):
    profile = models.ForeignKey(
        'users.Profile',
        related_name='academic_formation',
        on_delete=models.CASCADE,
        verbose_name='Perfil',
    )
    educational_institution = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name='Instituição de ensino',
    )
    course = models.CharField(
        max_length=80,
        db_index=True,
        blank=True,
        null=True,
        verbose_name='Curso'
    )
    knowledge_area = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name='Área do conhecimento'
    )
    started_at = models.DateTimeField(verbose_name="Iniciado em")
    ended_at = models.DateTimeField(verbose_name="Finalizado em")

    class Meta:
        verbose_name = 'Formação Acadêmica'
        verbose_name_plural = 'Formações acadêmicas'
        indexes = [
            models.Index(fields=['course']),
        ]

    def __str__(self):
        return str(self.pk)