import json

import core.esporte.models




class Esporte():
     def __init__(self, esporte = None):
         self.esporte = esporte



     def simular_aposta(self, campeonato_id=None, time_a=None, time_b=None, num_gols=None):
         eventos = core.esporte.models
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
