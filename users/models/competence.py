from django.db import models

from users.models.experience import Experience
from users.models.academic_formation import AcademicFormation


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

    def to_dict(self):
        return{
            'id': self.pk,
            'competence_name': self.competence_name,
            'experience': [exp.to_dict() for exp in self.experience.all()],
            'academic': [academic.to_dict() for academic in self.academic_formation.all()],
        }
    
    def update(self, context):
        if context.get('competence_name'):
            self.competence_name = context.get('competence_name')

        experience_list = context.get('experience_list')
        if experience_list:
            for exp in self.experience.all():
                if exp.id not in experience_list:
                    self.experience.remove(exp)

            for experience in experience_list:
                self.experience.add(Experience.objects.filter(id=experience).first())


        academic_list = context.get('academic_list')
        if academic_list:
            for acad in self.academic_formation.all():
                if acad.id not in academic_list:
                    self.academic_formation.remove(acad)
                    
            for academic in academic_list:
                self.academic_formation.add(AcademicFormation.objects.filter(id=academic).first())


        self.save()
        return self.to_dict()

    
    class Meta:
        verbose_name = 'Competência'
        verbose_name_plural = 'Competências'
        indexes = [
            models.Index(fields=['competence_name']),
        ]

    def __str__(self):
        return str(self.pk)
