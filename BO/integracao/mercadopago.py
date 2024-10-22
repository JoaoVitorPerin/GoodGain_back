import market
import datetime
from datetime import timedelta
import requests
from django.utils.timezone import make_aware
from BO.integracao.integracao import Integracao
import core.esporte.models
import json
import zoneinfo
class Mercadopago(Integracao):
    import requests

    def create_subscription(payer_email, preapproval_plan_id=None, reason=None, external_reference=None):
        url = "https://api.example.com/v1/subscriptions"  # Substitua com a URL correta do endpoint
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Substitua YOUR_ACCESS_TOKEN pelo seu token de acesso
        }

        # Monta o corpo da requisição
        data = {
            "payer_email": payer_email
        }

        # Adiciona campos opcionais se fornecidos
        if preapproval_plan_id:
            data["preapproval_plan_id"] = preapproval_plan_id
        if reason:
            data["reason"] = reason
        if external_reference:
            data["external_reference"] = external_reference

        response = requests.post(url, headers=headers, json=data)
        return response.json()

    # Exemplo de uso da função
    response = create_subscription(
        payer_email="test_user@testuser.com",
        preapproval_plan_id="2c938084726fca480172750000000000",
        reason=reason,
        external_reference="YG-1234"
    )
    print(response)

    def search_subscriptions(q=None, payer_id=None, payer_email=None, preapproval_plan_id=None):
        url = "https://api.mercadopago.com/preapproval/search"  # URL para buscar assinaturas
        headers = {
            'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Substitua YOUR_ACCESS_TOKEN pelo seu token de acesso
        }

        # Monta os parâmetros de consulta
        params = {}
        if q:
            params['q'] = q
        if payer_id:
            params['payer_id'] = payer_id
        if payer_email:
            params['payer_email'] = payer_email
        if preapproval_plan_id:
            params['preapproval_plan_id'] = preapproval_plan_id

        # Envia a requisição GET
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    # Exemplo de uso da função
    response = search_subscriptions(
        q="Plan gold",
        payer_id=123123123,
        payer_email="test_1234@testuser.com",
        preapproval_plan_id="fa"
    )
    print(response)