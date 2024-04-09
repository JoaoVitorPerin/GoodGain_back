from BO.integracao.integracao import Integracao
import json


class Sportradar(Integracao):
    def __init__(self, key=None):
        self.key = key

    def pegar_versus(self):
        self.url = "https://api.sportradar.com/soccer-extended/trial/v4/pt/competitors/sr%3Acompetitor%3A44/versus/sr%3Acompetitor%3A42/summaries.json?api_key=uZYxYmzpVM89nwOKkd3Ao69uu1PXjt4vaDFhnXcD"

        self.headers = {"accept": "application/json"}
        self.body = {}
        self.get(dumps=False)

        return json.loads(self.response)
