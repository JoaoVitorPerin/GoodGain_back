from django.shortcuts import get_object_or_404

import BO.cliente.cliente
import BO.esporte
class Aposta():
    def __init__(self, campeonato=None, timeA=None, timeB=None, valor=None, odd=None):
        self.campeonato = campeonato
        self.timeA = timeA
        self.timeB = timeB
        self.valor = valor
        self.odd = odd

    def enviarAposta(self, cliente_id, campeonato_id, timeA, timeB, valor, odd):
        try:
            cliente = BO.cliente.cliente.Cliente.get_cliente(cliente_id)
            if not cliente:
                return False, 'Usuário não encontrado no sistema!'

            aposta = Aposta(
                cliente=cliente,
                campeonato=campeonato_id,
                timeA=timeA,
                timeB=timeB,
                valor=valor,
                odd=odd
            )
            aposta.save()

            return {"status": "success", "message": "Aposta enviada com sucesso!"}

        except Exception as e:
            return {"status": "error", "message": str(e)}