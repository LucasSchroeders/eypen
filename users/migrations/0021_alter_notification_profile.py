# Generated by Django 3.2.13 on 2023-10-01 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20230930_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='users.profile', verbose_name='Perfil'),
        ),
    ]