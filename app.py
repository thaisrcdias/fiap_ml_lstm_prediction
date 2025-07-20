import json
import os

import uvicorn
from fastapi import FastAPI
from fastapi import Response
from datetime import datetime


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from tensorflow.keras.models import load_model
import joblib

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

    if not isinstance(prices, list) or len(prices) < WINDOW_SIZE:
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
    return {"predicted_close": float(pred[0, 0])}

@app.get("/healthcheck")
def healthcheck():
    """Health check endpoint to verify API status."""
    return {
        "message": "OK",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/")
async def root() -> Response:
    return Response(content=json.dumps({"Status": "OK"}), media_type="application/json", status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))