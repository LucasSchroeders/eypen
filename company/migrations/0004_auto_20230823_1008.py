# Generated by Django 3.2.13 on 2023-08-23 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_alter_company_business_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_position', models.CharField(db_index=True, max_length=80, verbose_name='Cargo')),
                ('seniority', models.CharField(choices=[('jovem_aprediz', 'Jovem Aprendiz'), ('estagiario', 'Estágiario'), ('junior', 'Júnior'), ('pleno', 'Pleno'), ('senior', 'Sênior'), ('especialista', 'Especialista')], max_length=30, verbose_name='Senioridade')),
                ('job_modality', models.CharField(choices=[('presencial', 'Presencial'), ('hibrido', 'Híbrido'), ('home_office', 'Home Office')], max_length=50, verbose_name='Modalidade')),
                ('job_type', models.CharField(choices=[('autonomo', 'Autônomo'), ('clt', 'CLT'), ('freelance', 'Freelance'), ('estagio', 'Estágio'), ('aprendiz', 'Aprendiz'), ('trainee', 'Trainee')], max_length=50, verbose_name='Tipo de trabalho')),
                ('state', models.CharField(blank=True, choices=[('SP', 'São Paulo'), ('RJ', 'Rio de Janeiro'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=200, null=True, verbose_name='Estado')),
                ('city', models.CharField(blank=True, max_length=200, null=True, verbose_name='Cidade')),
                ('description', models.CharField(max_length=2000, verbose_name='Descrição')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='company.company', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Vaga',
                'verbose_name_plural': 'Vagas',
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.IntegerField(verbose_name='Número da etapa')),
                ('title', models.CharField(db_index=True, max_length=80, verbose_name='Nome da etapa')),
                ('step_modality', models.CharField(max_length=50, verbose_name='Modalidade')),
                ('step_type', models.CharField(max_length=80, verbose_name='Tipo da etapa')),
                ('step_vulnerability', models.CharField(max_length=80, verbose_name='Para quem é a etapa')),
                ('description', models.CharField(max_length=2000, verbose_name='Descrição')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='company.vacancy', verbose_name='Vagas')),
            ],
            options={
                'verbose_name': 'Etapa',
                'verbose_name_plural': 'Etapas',
            },
        ),
        migrations.AddIndex(
            model_name='vacancy',
            index=models.Index(fields=['job_position'], name='company_vac_job_pos_6a66f0_idx'),
        ),
        migrations.AddIndex(
            model_name='step',
            index=models.Index(fields=['title'], name='company_ste_title_4bcac8_idx'),
        ),
    ]
