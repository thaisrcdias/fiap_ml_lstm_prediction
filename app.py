import json
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi import Response
from datetime import datetime


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model
import joblib
from ddtrace import patch_all; patch_all()


app = FastAPI(
    title="Bitcoin LSTM Predictor API",
    description="API para previsão do preço do Bitcoin usando LSTM",
    version="1.0.0"
)

# Carregar o modelo e o scaler
model = load_model("./lstm_bitcoin.h5")
scaler = joblib.load("./scaler.save")
WINDOW_SIZE = 60 

class PriceRequest(BaseModel):
    prices: list

@app.post("/predict")
def predict_price(request: PriceRequest):
    prices = request.prices
    send_log_to_datadog(f"Recebida previsão com {len(prices)} valores.", level="info")
    if not isinstance(prices, list) or len(prices) < WINDOW_SIZE:
        send_log_to_datadog("Envie ao menos {WINDOW_SIZE} preços no formato de lista.", level="error")
        raise HTTPException(
            status_code=400, 
            detail=f"Envie ao menos {WINDOW_SIZE} preços no formato de lista."
        )
    # Preprocessamento: normalizar os dados com o scaler treinado
    prices_np = np.array(prices).reshape(-1, 1)
    prices_scaled = scaler.transform(prices_np)
    X_input = prices_scaled[-WINDOW_SIZE:].reshape(1, WINDOW_SIZE, 1)
    pred_scaled = model.predict(X_input)
    pred = scaler.inverse_transform(pred_scaled)
    send_log_to_datadog("Previsão realizada com sucesso!", level="info")
    return {"predicted_close": float(pred[0, 0])}

@app.get("/healthcheck")
def healthcheck():
    """Health check endpoint to verify API status."""
    return {
        "message": "OK",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    send_log_to_datadog(f"Erro na API: {str(exc)}", level="error")
    return {"detail": "Erro interno na API"}

import requests
import json

# Exemplo de uso:
DATADOG_API_KEY = "be3f70070c8f88b11511ac9750d2af8b"
def send_log_to_datadog(message, level="info"):
    url = "https://http-intake.logs.datadoghq.com/v1/input"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": DATADOG_API_KEY
    }
    log_entry = {
        "message": message,
        "ddsource": "python",
        "service": "bitcoin-lstm-api",
        "status": level
    }
    try:
        requests.post(url, headers=headers, data=json.dumps(log_entry), timeout=3)
    except Exception as e:
        print(f"Falha ao enviar log para Datadog: {e}")



@app.get("/")
async def root() -> Response:
    return Response(content=json.dumps({"Status": "OK"}), media_type="application/json", status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))