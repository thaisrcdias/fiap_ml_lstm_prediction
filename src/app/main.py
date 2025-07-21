import os
import logging
import sys

# Garante que o diretório raiz está no path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.chdir('app')

print("Diretório atual:", os.getcwd())
print("Conteúdo:", os.listdir())

import json
import pickle
import yfinance as yf
from datetime import datetime, timedelta
# from models.utils.transformers import *


# print("Diretório atual:", os.getcwd())
# print("Diretório atual:", os.listdir('models/utils'))

# Carrega modelo ao iniciar
MODEL_PATH = "models/pipeline_model_LSTM.pkl"
pipe = pickle.load(open(MODEL_PATH, "rb"))



def lambda_handler(event, context):
    try:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s:%(funcName)s:%(message)s"
        )

        # Input vem no body em formato JSON
        body = json.loads(event.get("body", "{}"))
        data = body.get("date")
        logging.info(f"Data recebida: {data}")

        if not data:
            logging.error("Campo 'date' ausente no corpo da requisição")
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'date' field"})
            }

        # Define o intervalo para pegar os dados
        symbol = 'BTC-USD'
        start_date = (datetime.strptime(data, '%Y-%m-%d') - timedelta(days=70)).strftime('%Y-%m-%d')
        end_date = (datetime.strptime(data, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

        # Baixa os dados
        X = yf.download(symbol, start=start_date, end=end_date)
        logging.info(f"Dados baixados para o período de {start_date} a {end_date}")

        # Verificação simples
        if X.empty:
            logging.error("Nenhum dado retornado do Yahoo Finance")
            return {
                "statusCode": 422,
                "body": json.dumps({"error": "No data returned from Yahoo Finance"})
            }

        # Faz predição
        logging.info("Fazendo predição com o modelo")
        score = pipe.predict(X)
        logging.info(f"Predição realizada: {score}")

        return {
            "statusCode": 200,
            "body": json.dumps({"prediction": score.get('valor_predito')})
        }

    except Exception as e:
        logging.error(f"Erro ao processar a requisição: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
