import datetime
import json

import core.esporte.models




class Esporte():
     def __init__(self, esporte = None):
         self.esporte = esporte



     # def simular_aposta(self, campeonato_id=None, time_a=None, time_b=None, num_gols=None):
     #     eventos = core.esporte.models
     def get_log(self,operacao=None):
         try:
             if operacao:
                logs = list(core.esporte.models.Log.objects.values().filter(tipo_operacao=operacao).order_by('id'))
             else:
                logs =list(core.esporte.models.Log.objects.values().order_by('id'))
             return logs
         except:
             return []

     def get_operacoes(self, ):
         try:
             operacoes = list(core.esporte.models.Log.objects.values_list('tipo_operacao').distinct('tipo_operacao'))
             return operacoes
         except:
             return []
     def get_eventos(self):
        try:
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
             campeonatos = list(core.esporte.models.Campeonato.objects.values())
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
