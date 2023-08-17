# Generated by Django 3.2.13 on 2023-08-17 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20230817_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='business_area',
            field=models.CharField(blank=True, choices=[('hotel', 'Hotelaria'), ('adm_sup_services', 'Serviços administrativos e suporte'), ('construction', 'Construção'), ('consumer_services', 'Atendimento ao consumidor'), ('education', 'Educação'), ('entertainment', 'Entreterimento'), ('farm_services', 'Agricultura, pecuária, silvicultura'), ('financial_services', 'Serviços financeiros'), ('holding_companies', 'Seguradoras'), ('hospitals_health_care', 'Hospitais e atendimento à saúde'), ('Manufacturing', 'Manufatura'), ('oil_gas_mining', 'Petróleo, gás e mineração'), ('professional_services', 'Serviços profissionais'), ('rental_services', 'Serviços de alguel'), ('retail', 'Varejo'), ('tech_info_media', 'Tecnologia, informação e internet'), ('trans_log_sup_stor', 'Transporte, logística, cadeia de suprimentos e armazenamento'), ('utilities', 'Serviços de eletricidade, gás, água e esgoto'), ('wholesale', 'Atacado')], max_length=80, null=True, verbose_name='Areas de atuação'),
        ),
    ]