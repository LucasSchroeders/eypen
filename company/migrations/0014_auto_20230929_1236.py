# Generated by Django 3.2.13 on 2023-09-29 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_profile_curriculum'),
        ('company', '0013_alter_step_step_vulnerability'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='candidates_step',
            field=models.ManyToManyField(related_name='vacancies_step', to='users.Profile', verbose_name='Candidatos da etepa'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='approved_candidates',
            field=models.ManyToManyField(related_name='vacancies_approved', to='users.Profile', verbose_name='Candidatos aprovados'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='candidates',
            field=models.ManyToManyField(related_name='vacancies', to='users.Profile', verbose_name='Candidatos'),
        ),
    ]