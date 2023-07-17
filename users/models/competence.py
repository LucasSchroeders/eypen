from django.db import models


class Competence(models.Model):
    profile = models.ForeignKey(
        'users.Profile',
        related_name='competence',
        on_delete=models.PROTECT,
        verbose_name='Competência',
    )
    competence_name = models.CharField(
        max_length=50,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="Competência",
    )
    experience = models.ForeignKey(
        'users.Experience',
        on_delete=models.PROTECT,
        verbose_name='Experiência',
    )
    academic_formation = models.ForeignKey(
        'users.AcademicFormation',
        on_delete=models.PROTECT,
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
