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
    status = models.BooleanField(null=True, default=True)



    class Meta:
        db_table = u'"public\".\"esporte"'


class Tipo(models.Model):
    """
    :Nome da classe/função: Esportes
    :descrição: Classe de esportes
    :Criação: Thiago Jungles Caron - 16/04/2024
    :Edições:
    """
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=100, null=True)
    informacao = models.CharField(max_length=100, null=True)
    tipo = models.CharField(max_length=100, null=True)
    status = models.BooleanField(null=True, default=True)


    class Meta:
        db_table = u'"public\".\"tipo"'

# class Season(models.Model):
#     """
#     :Nome da classe/função: Season
#     :descrição: Classe de seasons
#     :Criação: Thiago Jungles Caron - 16/04/2024
#     :Edições:
#     """
#     id = models.CharField(primary_key=True)
#     nome = models.CharField(max_length=100, null=True)
#     dat_inicio = models.CharField(max_length=100, null=True)
#     dat_fim = models.CharField(max_length=100, null=True)
#     status = models.BooleanField(null=True, default=True)
#
#
#
#     class Meta:
#         db_table = u'"public\".\"season"'


class PerformaceTime(models.Model):
    """
    :Nome da classe/função: PerformaceTime
    :descrição: Classe de performace dos times em uma determinada season
    :Criação: Thiago Jungles Caron - 16/04/2024
    :Edições:
    """
    season = models.CharField(max_length=100, null=True)
    time = models.ForeignKey('esporte.Time', on_delete=models.DO_NOTHING, null=True)
    info = models.CharField(max_length=20000,null=True)
    status = models.BooleanField(null=True, default=True)



    class Meta:
        db_table = u'"public\".\"performace_time"'

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
    status = models.BooleanField(null=True, default=True)
    season_atual = models.CharField(max_length=100, null=True)



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
    logo = models.CharField(max_length=200, null=True)
    status = models.BooleanField(null=True, default=True)



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
    data = models.CharField(null=True)
    time_a = models.ForeignKey('esporte.Time', on_delete=models.DO_NOTHING, null=True, related_name='time_a')
    time_b = models.ForeignKey('esporte.Time', on_delete=models.DO_NOTHING, null=True, related_name='time_b')
    resultado_time_a = models.CharField(max_length=500,null=True)
    resultado_time_b = models.CharField(max_length=500,null=True)
    resultado_partida = models.CharField(null=True, max_length=100000)
    campeonato = models.ForeignKey('esporte.Campeonato', on_delete=models.DO_NOTHING, null=True)
    season = models.CharField(max_length=100, null=True)
    status = models.BooleanField(null=True, default=True)

    class Meta:
        db_table = u'"public\".\"evento"'


class Log(models.Model):
    """
        :Nome da classe/função: Log
        :descrição: Classe de logs do sistema será utilizada para armazenar retorno da API após fazer o cron
        :Criação: Thiago Jungles Caron - 01/08/2024
        :Edições:
        """
    data = models.CharField(null=True)
    status = models.BooleanField(null=True, default=True)
    informacao = models.CharField(max_length=200,null=True)
    tipo_operacao = models.CharField(max_length=100,null=True)
    class Meta:
        db_table = u'"public\".\"log"'