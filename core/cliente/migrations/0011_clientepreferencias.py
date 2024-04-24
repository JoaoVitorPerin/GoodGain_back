# Generated by Django 5.0.3 on 2024-04-24 23:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0010_delete_clientepreferencias'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientePreferencias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esporte', models.CharField(max_length=500, null=True)),
                ('campeonato', models.CharField(max_length=500, null=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('opcoes_apostas', models.CharField(max_length=500, null=True)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cliente.cliente')),
            ],
            options={
                'db_table': '"public"."cliente_preferencias"',
            },
        ),
    ]