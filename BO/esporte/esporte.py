import datetime
import json
import ast
import BO.integracao.apifootball

import core.esporte.models
import core.cliente.models

class Esporte():
     def __init__(self, esporte = None):
         self.esporte = esporte



     # def simular_aposta(self, campeonato_id=None, time_a=None, time_b=None, num_gols=None):
     #     eventos = core.esporte.models
     def get_log(self,operacao=None):
         try:
             if operacao:
                logs = list(core.esporte.models.Log.objects.values().filter(tipo_operacao=operacao).order_by('-id'))
             else:
                logs =list(core.esporte.models.Log.objects.values().order_by('-id'))
             return logs
         except:
             return []

     def get_predicoes(self, evento_id=None):
         predicoes = BO.integracao.apifootball.Apifootball().get_predictions(evento_id=evento_id)
         return predicoes['response'][0]['predictions']
     def get_odds(self, evento=None, tipo_aposta=None):
         odds_evento = BO.integracao.apifootball.Apifootball().get_odds_evento(evento=evento)

         lista_odds = []
         #tratamento de odds de eventos
         codigos_relacionais = core.esporte.models.Tipo.objects.values('codigo_externo','informacao').filter(codigo=tipo_aposta, tipo='CODIGO.RELACIONAL.APIFOOTBALL').first()
         for casa_aposta in odds_evento['response'][0]['bookmakers']:
             for aposta_tipo in casa_aposta['bets']:
                 if aposta_tipo['id'] == int(codigos_relacionais.get('codigo_externo')):
                    for valor_odd in aposta_tipo['values']:
                        if str(valor_odd['value']) == codigos_relacionais.get('informacao'):
                            lista_odds.append({'nome':str(valor_odd['odd']) +' - '+ str(casa_aposta['name']),
                                               'valor_odd':float(valor_odd['odd'])})
         return lista_odds

     def get_live(self, evento=None):
         odds_evento = BO.integracao.apifootball.Apifootball().get_live_evento(evento=evento)
         return odds_evento

     def get_operacoes(self, ):
         try:
             operacoes = list(core.esporte.models.Log.objects.values_list('tipo_operacao').distinct('tipo_operacao'))
             return operacoes
         except:
             return []
     def get_eventos(self):
        try:
            data_hoje = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
            lista_eventos_atuais = list(core.esporte.models.Evento.objects.values('id',
                                                            'data',
                                                            'time_a',
                                                            'time_b',
                                                            'resultado_time_a',
                                                            'resultado_time_b',
                                                            'resultado_partida',
                                                            'campeonato',
                                                            'season','status','time_a__nome','time_b__nome','time_a__logo','time_b__logo','campeonato__nome').filter(data__gte=data_hoje).order_by('data'))
            dict_evento_campeonato = {}
            for evento in lista_eventos_atuais:
                lista_eventos = []
                if evento['campeonato'] not in dict_evento_campeonato:
                    dict_evento_campeonato[evento['campeonato']] = {'nome': 'str', 'eventos': []}
                    lista_eventos.append(evento)
                    dict_evento_campeonato[evento['campeonato']]['eventos'] = lista_eventos
                    dict_evento_campeonato[evento['campeonato']]['nome'] = evento['campeonato__nome']
                else:
                    lista_eventos = dict_evento_campeonato[evento['campeonato']]['eventos']
                    lista_eventos.append(evento)
                    dict_evento_campeonato[evento['campeonato']]['eventos'] = lista_eventos
                lista_eventos = []
            lista_eventos_informativos = []
            for evento_informativo in dict_evento_campeonato:
                lista_eventos_informativos.append(dict_evento_campeonato[evento_informativo])
            return True, lista_eventos_informativos
        except:
            return False, []

     def get_eventos_campeonato(self, user=None):
        try:
            data_hoje = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
            preferencias = list(core.cliente.models.ClientePreferencias.objects.values('id_preferencia').filter(cliente_id=user.cpf,tipo_preferencia='campeonato'))
            lista_campeonatos = []
            for preferencia in preferencias:
                lista_campeonatos.append(preferencia['id_preferencia'])
            if lista_campeonatos==[]:
                lista_eventos_campeonatos = list(core.esporte.models.Evento.objects.values('id',
                                                                'data',
                                                                'time_a',
                                                                'time_b',
                                                                'resultado_time_a',
                                                                'resultado_time_b',
                                                                'resultado_partida',
                                                                'campeonato',
                                                                'campeonato__nome',
                                                                'season','status','time_a__nome','time_b__nome','time_a__logo','time_b__logo','campeonato__nome').filter(data__gte=data_hoje).order_by('data'))
            else:
                lista_eventos_campeonatos = list(core.esporte.models.Evento.objects.values('id',
                                                                               'data',
                                                                               'time_a',
                                                                               'time_b',
                                                                               'resultado_time_a',
                                                                               'resultado_time_b',
                                                                               'resultado_partida',
                                                                               'campeonato',
                                                                               'campeonato__nome',
                                                                               'season', 'status', 'time_a__nome',
                                                                               'time_b__nome', 'time_a__logo',
                                                                               'time_b__logo',
                                                                               'campeonato__nome').filter(
                    data__gte=data_hoje,campeonato_id__in=lista_campeonatos).order_by('data'))

            dict_evento_campeonato = {}
            for evento in lista_eventos_campeonatos:
                lista_eventos = []
                if evento['campeonato'] not in dict_evento_campeonato:
                   dict_evento_campeonato[evento['campeonato']] = {'nome':'str','eventos':[]}
                   lista_eventos.append(evento)
                   dict_evento_campeonato[evento['campeonato']]['eventos'] = lista_eventos
                   dict_evento_campeonato[evento['campeonato']]['nome'] = evento['campeonato__nome']
                else:
                   lista_eventos = dict_evento_campeonato[evento['campeonato']]['eventos']
                   lista_eventos.append(evento)
                   dict_evento_campeonato[evento['campeonato']]['eventos'] = lista_eventos
                lista_eventos = []
            lista_eventos_informativos = []
            for evento_informativo in dict_evento_campeonato:
                lista_eventos_informativos.append(dict_evento_campeonato[evento_informativo])
            return True, lista_eventos_informativos
        except:
            return False, []

     def get_eventos_recomendados(self,cliente=None):
        try:
            core.cliente.models.ClientePreferencias.objects.values().filter(cliente_id=cliente.pk)
            data_hoje = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
            lista_eventos = list(core.esporte.models.Evento.objects.values('id',
                                                            'data',
                                                            'time_a',
                                                            'time_b',
                                                            'resultado_time_a',
                                                            'resultado_time_b',
                                                            'resultado_partida',
                                                            'campeonato',
                                                            'season','status','time_a__nome','time_b__nome','time_a__logo','time_b__logo','campeonato__nome').filter(data__gte=data_hoje).order_by('data'))
            return True, lista_eventos
        except:
            return False, []
     def get_campeonatos(self):
         try:
             campeonatos = list(core.esporte.models.Campeonato.objects.filter(status=True).values())
             return True, campeonatos
         except:
            return False, []

     def get_times_campeonato(self, campeonato_id=None):
         try:
             lista_times_ids = []
             eventos_campeonato = list(core.esporte.models.Evento.objects.values().filter(campeonato_id=campeonato_id))
             for evento in eventos_campeonato:
                 if evento.get('time_a_id') not in lista_times_ids:
                     lista_times_ids.append(evento.get('time_a_id'))
                 if evento.get('time_b_id') not in lista_times_ids:
                     lista_times_ids.append(evento.get('time_b_id'))

             # times = list(core.esporte.models.Time.objects.values().filter(id__in=lista_times_ids))
             performance_times = list(core.esporte.models.PerformaceTime.objects.values().filter(time_id__in=lista_times_ids))
             lista_performace_times = []
             for performace in performance_times:
                 performace['info'] = json.loads(performace['info'])
             return True, performance_times
         except:
             return False, []

     def get_campeonatos_api(self):
         try:
             campeonatos = BO.integracao.apifootball.Apifootball().get_todos_campeonatos()["response"]
             campeonatos_filtrados = [
                 {
                     'id': campeonato['league']['id'],
                     'name': f"{campeonato['league']['name']} - ({campeonato['country']['name']})"
                 }
                 for campeonato in campeonatos
             ]
             return True, campeonatos_filtrados
         except:
             return False, []

     def enviar_campeonato(self, nome=None,campeonato_id=None, season=None):
         try:
             campeonato = core.esporte.models.Campeonato()
             campeonato.nome = nome
             campeonato.id = campeonato_id
             campeonato.esporte_id = 1
             campeonato.season_atual = season
             campeonato.save()
             return True, 'Campeonato cadastrado com sucesso!'
         except:
             return False, 'Erro ao cadastrar campeonato!'

     def deletar_campeonato(self, campeonato_id=None):
        try:
            campeonato = core.esporte.models.Campeonato.objects.filter(id=campeonato_id).first()
            campeonato.status = False
            campeonato.save()
            return True, 'Campeonato deletado com sucesso'
        except:
            return False, 'Erro ao deletar campeonato!'

     def editar_campeonato(self, campeonato_id=None, nome=None, season=None):
         try:
             campeonato = core.esporte.models.Campeonato.objects.filter(id=campeonato_id).first()
             if not campeonato:
                 return False, 'Campeonato nao encontrado!'
             if nome:
                 campeonato.nome = nome
             if season:
                 campeonato.season_atual = season
             campeonato.status = True
             campeonato.save()
             return True, 'Campeonato editado com sucesso!'
         except:
             return False, 'Erro ao editar campeonato!'