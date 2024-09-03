import datetime
from datetime import timedelta
import requests
from django.utils.timezone import make_aware
from BO.integracao.integracao import Integracao
import core.esporte.models
import json


class Apifootball(Integracao):

    def __init__(self, key=None):
        self.key = 'FBQqo7FJT11AEVIR7xCaP2SaNi5LOo2Y9TX92WYf'

        self.headers = {"x-rapidapi-key": "395b0fdfdfmshd8650bb40aff08dp1bf0f3jsnca2d0c8b1c4b",
                        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"}

    def get_info_jogos(self,evento_id=None):
        self.url ="/v3/fixtures/events?fixture={}".format(evento_id)
        params = {}
        self.response = requests.get(self.url, headers=self.headers, params=params).json()

        return self.response

    def jogos_dia_liga(self, liga="71",season="2024", date="2024-08-03"):
        self.url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {"date":date,
                     "league":liga,
                     "season":season}
        self.response = requests.get(self.url, headers=self.headers, params=params).json()

        return self.response

    def performace_time(self, liga="72",season="2024", time="147"):
        self.url = "https://api-football-v1.p.rapidapi.com/v3/teams/statistics"
        params = {"team":time,
                  "league":liga,
                  "season":season}
        self.response = requests.get(self.url, headers=self.headers, params=params).json()

        return self.response


    def get_info_evento(self, evento_id=None):
        self.url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?id=[[evento_id]]".replace('[[evento_id]]', evento_id)
        params = {"id": evento_id,}
        self.response = requests.get(self.url, headers=self.headers, params=params).json()
        return self.response

    def todas_ligas(self, liga="71",season="2024", date="2024-08-03"):
        self.url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
        params = {}
        self.response = requests.get(self.url, headers=self.headers, params=params).json()

        return self.response

    def get_odds_evento(self, evento=None):
        self.url = "https://api-football-v1.p.rapidapi.com/v3/odds?fixture=[[evento_id]]".replace('[[evento_id]]', evento)
        params = {"fixture": evento}
        self.response = requests.get(self.url, headers=self.headers, params=params).json()
        return self.response

    def get_live_evento(self, evento=None):
        self.url = "https://api-football-v1.p.rapidapi.com/v3/fixtures?live=all&ids=[[evento_id]]".replace('[[evento_id]]', evento)
        # params = {"ids": evento}
        self.response = requests.get(self.url, headers=self.headers).json()
        return self.response

    def atualizar_eventos_ocorridos(self):
        try:
            # Pega a data e hora atual
            now = datetime.datetime.now()
            # Define start_date para 00:01 do dia anterior
            start_date = make_aware(datetime.datetime.combine(now.date() - timedelta(days=1), datetime.datetime.min.time())) + timedelta(
                minutes=1)
            # Define end_date para 23:59 do dia atual
            end_date = make_aware(datetime.datetime.combine(now.date(), datetime.datetime.max.time())) - timedelta(minutes=1)

            eventos = list(core.esporte.models.Evento.objects.filter(data__range=(start_date, end_date)))
            dados = {}
            for evento in eventos:
                dados[evento.id] = self.get_info_evento(evento_id=evento.id)
                evento.resultado_partida = json.dumps(dados[evento.id]['response'])
                evento.save()
            return True
        except:
            return False
    def atualizar_base(self, data=None):
        try:
            operacao = 'coleta campeonatos'
            if not data:
                datetime_hoje = datetime.datetime.now().strftime('%Y-%m-%d')
            else:
                datetime_hoje = data
            campeonatos = list(core.esporte.models.Campeonato.objects.values().filter(status=True))

            for campeonato in campeonatos:
                operacao = 'coleta campeonatos_apifootball'
                resposta_atual = self.jogos_dia_liga(liga=campeonato.get('id'), date=datetime_hoje, season=campeonato.get('season_atual'))

                operacao = 'cadastro_times_apifootball'
                for response in resposta_atual.get('response'):
                    response.get('teams').get('home').get('id')
                    response.get('teams').get('away').get('id')
                    time_casa = core.esporte.models.Time.objects.values().filter(id=response.get('teams').get('home').get('id'))
                    time_fora = core.esporte.models.Time.objects.values().filter(id=response.get('teams').get('away').get('id'))
                    if not time_casa:
                        novo_time = core.esporte.models.Time()
                        novo_time.id = response.get('teams').get('home').get('id')
                        novo_time.logo = response.get('teams').get('home').get('logo')
                        novo_time.nome = response.get('teams').get('home').get('name')
                        novo_time.save()
                    if not time_fora:
                        novo_time = core.esporte.models.Time()
                        novo_time.id = response.get('teams').get('away').get('id')
                        novo_time.logo = response.get('teams').get('away').get('logo')
                        novo_time.nome = response.get('teams').get('away').get('name')
                        novo_time.save()
                    operacao = 'cadastro_performace_times_apifootball'
                    performace_time_casa = self.performace_time(liga=campeonato.get('id'), time=response.get('teams').get('home').get('id'),season=campeonato.get('season_atual'))
                    performace_time_fora = self.performace_time(liga=campeonato.get('id'),
                                                                time=response.get('teams').get('away').get('id'),
                                                                season=campeonato.get('season_atual'))
                    performace_time_casa_dados = core.esporte.models.PerformaceTime.objects.filter(time_id=response.get('teams').get('home').get('id'),season=response.get('league').get('season')).first()
                    if not performace_time_casa_dados:
                        performace_time_casa_dados = core.esporte.models.PerformaceTime()
                        performace_time_casa_dados.season = response.get('league').get('season')
                        performace_time_casa_dados.time_id = response.get('teams').get('home').get('id')
                    performace_time_casa_dados.info = json.dumps(performace_time_casa['response'])
                    performace_time_casa_dados.save()

                    performace_time_fora_dados = core.esporte.models.PerformaceTime.objects.filter(
                        time_id=response.get('teams').get('away').get('id'),
                        season=response.get('league').get('season')).first()
                    if not performace_time_fora_dados:
                        performace_time_fora_dados = core.esporte.models.PerformaceTime()
                        performace_time_fora_dados.season = response.get('league').get('season')
                        performace_time_fora_dados.time_id = response.get('teams').get('away').get('id')
                    performace_time_fora_dados.info =  json.dumps(performace_time_fora['response'])
                    performace_time_fora_dados.save()

                    operacao = 'cadastro_eventos_apifootball'
                    evento = core.esporte.models.Evento.objects.filter(id=response.get('fixture').get('id')).first()
                    if not evento:
                        evento = core.esporte.models.Evento()
                        evento.id = response.get('fixture').get('id')



                    evento.data =  response.get('fixture').get('date')
                    evento.time_a_id = response.get('teams').get('home').get('id')
                    evento.time_b_id = response.get('teams').get('away').get('id')
                    evento.campeonato_id = response.get('league').get('id')
                    evento.season = response.get('league').get('season')
                    evento.save()


            log = core.esporte.models.Log()
            log.data = datetime.datetime.now().strftime('%Y-%m-%d')
            log.status = True
            log.tipo_operacao = 'atualizacao da base completa'
            log.informacao = 'sucesso'
            log.save()
            return True
        except:
            log = core.esporte.models.Log()
            log.data = datetime.datetime.now().strftime('%Y-%m-%d')
            log.status = True
            log.tipo_operacao = operacao
            log.informacao = 'erro na operação'
            log.save()
            return False