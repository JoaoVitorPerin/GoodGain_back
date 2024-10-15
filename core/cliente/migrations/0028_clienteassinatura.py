# Generated by Django 5.0.3 on 2024-10-15 18:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0027_perfis_valor_clientecarteira'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClienteAssinatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=40, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('acao', models.CharField(max_length=1000, null=True)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('perfil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cliente.perfis')),
            ],
            options={
                'db_table': '"public"."log_assinaturas"',
            },
        ),
    ]