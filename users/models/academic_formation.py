from django.db import models

from users.utils import string_to_date


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

    def to_dict(self):
        return {
            'id': self.pk,
            'educational_institution': self.educational_institution,
            'course': self.course,
            'knowledge_area': self.knowledge_area,
            'started_at': self.started_at,
            'ended_at': self.ended_at,
        }
    
    def update(self, context):
        if context.get('educational_institution'):
            self.educational_institution = context.get('educational_institution')

        if context.get('course'):
            self.course = context.get('course')

        if context.get('knowledge_area'):
            self.knowledge_area = context.get('knowledge_area')

        if context.get('started_at'):
            started_at = string_to_date(context.get('started_at'))
            self.started_at = started_at

        if context.get('ended_at'):
            ended_at = string_to_date(context.get('ended_at'))
            self.ended_at = ended_at
        
        self.save()
        return self.to_dict()

    class Meta:
        verbose_name = 'Formação Acadêmica'
        verbose_name_plural = 'Formações acadêmicas'
        indexes = [
            models.Index(fields=['course']),
        ]

    def __str__(self):
        return str(self.pk)