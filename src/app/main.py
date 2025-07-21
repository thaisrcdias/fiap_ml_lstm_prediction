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

print('a')

def lambda_handler(event, context):
    try:
        # Input vem no body em formato JSON
        body = json.loads(event.get("body", "{}"))
        data = body.get("date")

        if not data:
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

        # Verificação simples
        if X.empty:
            return {
                "statusCode": 422,
                "body": json.dumps({"error": "No data returned from Yahoo Finance"})
            }

        # Faz predição
        print('b')
        score = pipe.predict(X)

        return {
            "statusCode": 200,
            "body": json.dumps({"prediction": score.get('valor_predito')})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
