from django.db import models


class Competence(models.Model):
    profile = models.ForeignKey(
        'users.Profile',
        related_name='competence',
        on_delete=models.CASCADE,
        verbose_name='perfil',
    )
    competence_name = models.CharField(
        max_length=50,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="Competência",
    )
    experience = models.ManyToManyField(
        'users.Experience',
        verbose_name='Experiência',
    )
    academic_formation = models.ManyToManyField(
        'users.AcademicFormation',
        verbose_name='Formação Acadêmica',
    )
    
    class Meta:
        verbose_name = 'Competência'
        verbose_name_plural = 'Competências'
        indexes = [
            models.Index(fields=['competence_name']),
        ]

    def __str__(self):
        return str(self.pk)
