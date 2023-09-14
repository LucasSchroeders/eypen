# Generated by Django 3.2.13 on 2023-09-05 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_vacancy_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='status',
            field=models.CharField(blank=True, choices=[('ATV', 'Ativo'), ('PEN', 'Pendente'), ('ENC', 'Encerrado'), ('INTV', 'Inativo')], default='PEN', max_length=10, null=True, verbose_name='Status'),
        ),
    ]