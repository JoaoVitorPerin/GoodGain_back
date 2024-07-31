import datetime

import requests

from BO.integracao.integracao import Integracao
import core.esporte.models
import json


class Apifootball(Integracao):

    def __init__(self, key=None):
        self.key = 'FBQqo7FJT11AEVIR7xCaP2SaNi5LOo2Y9TX92WYf'

        self.headers = {"x-rapidapi-key": "395b0fdfdfmshd8650bb40aff08dp1bf0f3jsnca2d0c8b1c4b",
                        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"}

    def jogos_dia_liga(self, liga="71",season="2024", date="2024-08-03"):
        self.url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {"date":date,
                     "league":liga,
                     "season":season}
        self.response = requests.get(self.url, headers=self.headers, params=params).json()

        return self.response


    def todas_ligas(self, liga="71",season="2024", date="2024-08-03"):
        self.url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
        params = {}
        self.response = requests.get(self.url, headers=self.headers, params=params).json()

        return self.response

    def atualizar_base(self):
        try:
            campeonatos = list(core.esporte.models.Campeonato.objects.values().filter(status=True))
            datetime_hoje = datetime.datetime.now().strftime('%Y-%m-%d')
            for campeonato in campeonatos:
                resposta_atual = self.jogos_dia_liga(liga=campeonato.get('id'), date='2024-08-03', season=campeonato.get('season_atual'))

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
                    evento = core.esporte.models.Evento.objects.values().filter(id=response.get('fixture').get('id'))
                    if not evento:
                        evento = core.esporte.models.Evento()
                        evento.id = response.get('fixture').get('id')



                    evento.data =  response.get('fixture').get('date')
                    evento.time_a_id = response.get('teams').get('home').get('id')
                    evento.time_b_id = response.get('teams').get('away').get('id')
                    evento.campeonato_id = response.get('league').get('id')
                    evento.season = response.get('league').get('season')
                    evento.save()



            return True
        except:
            return False