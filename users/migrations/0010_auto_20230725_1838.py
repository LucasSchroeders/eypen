# Generated by Django 3.2.13 on 2023-07-25 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20230725_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competence',
            name='academic_formation',
            field=models.ManyToManyField(to='users.AcademicFormation', verbose_name='Formação Acadêmica'),
        ),
        migrations.RemoveField(
            model_name='competence',
            name='experience',
        ),
        migrations.AddField(
            model_name='competence',
            name='experience',
            field=models.ManyToManyField(to='users.Experience', verbose_name='Experiência'),
        ),
    ]
