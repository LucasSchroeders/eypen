# Generated by Django 3.2.13 on 2023-08-17 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_alter_company_business_area'),
        ('users', '0014_auto_20230814_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='company.company', verbose_name='Empresa'),
        ),
    ]
