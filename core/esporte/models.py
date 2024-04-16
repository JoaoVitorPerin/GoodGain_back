import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser



class Esporte(models.Model):
    """
    :Nome da classe/função: Esportes
    :descrição: Classe de esportes
    :Criação: Thiago Jungles Caron - 16/04/2024
    :Edições:
    """
    id = models.CharField(primary_key=True)
    nome = models.CharField(max_length=100, null=True)



    class Meta:
        db_table = u'"public\".\"esporte"'

class Campeonato(models.Model):
    """
    :Nome da classe/função: Campeonato
    :descrição: Classe de campeonatos
    :Criação: Thiago Jungles Caron - 16/04/2024
    :Edições:
    """
    id = models.CharField(primary_key=True)
    nome = models.CharField(max_length=100, null=True)
    esporte = models.ForeignKey('esporte.Esporte', on_delete=models.DO_NOTHING, null=True)



    class Meta:
        db_table = u'"public\".\"campeonato"'


class Time(models.Model):
    """
    :Nome da classe/função: Campeonato
    :descrição: Classe de campeonatos
    :Criação: Thiago Jungles Caron - 16/04/2024
    :Edições:
    """
    id = models.CharField(primary_key=True)
    nome = models.CharField(max_length=100, null=True)



    class Meta:
        db_table = u'"public\".\"time"'


class Evento(models.Model):
    """
    :Nome da classe/função: Evento
    :descrição: Classe de eventos
    :Criação: Thiago Jungles Caron - 16/04/2024
    :Edições:
    """
    id = models.CharField(primary_key=True)
    nome = models.CharField(max_length=100, null=True)
    data = models.IntegerField(null=True)
    time_a = models.ForeignKey('esporte.Time', on_delete=models.DO_NOTHING, null=True, related_name='time_a')
    time_b = models.ForeignKey('esporte.Time', on_delete=models.DO_NOTHING, null=True, related_name='time_b')
    resultado_time_a = models.ForeignKey('esporte.Time', on_delete=models.DO_NOTHING, null=True, related_name='resultado_time_a')
    resultado_time_b = models.ForeignKey('esporte.Time', on_delete=models.DO_NOTHING, null=True, related_name='resultado_time_b')
    campeonato = models.ForeignKey('esporte.Campeonato', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = u'"public\".\"evento"'

