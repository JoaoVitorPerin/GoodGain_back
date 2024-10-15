# import market
# import datetime
# from datetime import timedelta
# import requests
# from django.utils.timezone import make_aware
# from BO.integracao.integracao import Integracao
# import core.esporte.models
# import json
# import zoneinfo
#
#
# class Mercadopago(Integracao):
#
#     def pagar(self):
#         sdk = Mercadopago.SDK("ACCESS_TOKEN")
#
#         request_options = mercadopago.config.RequestOptions()
#         request_options.custom_headers = {
#             'x-idempotency-key': '<SOME_UNIQUE_VALUE>'
#         }
#
#         payment_data = {
#             "transaction_amount": float(request.POST.get("transaction_amount")),
#             "token": request.POST.get("token"),
#             "description": request.POST.get("description"),
#             "installments": int(request.POST.get("installments")),
#             "payment_method_id": request.POST.get("payment_method_id"),
#             "payer": {
#                 "email": request.POST.get("email"),
#                 "identification": {
#                     "type": request.POST.get("type"),
#                     "number": request.POST.get("number")
#                 }
#             }
#         }
#
#         payment_response = sdk.payment().create(payment_data, request_options)
#         payment = payment_response["response"]
#
#         print(payment)
