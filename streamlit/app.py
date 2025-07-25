import streamlit as st
import requests
from datetime import date

# Título
st.title("Previsão da moeda BitCoin ($)")

st.text("Insira a data que deseja fazer a predição. Ao inserir a data, a api irá extrair os últimos 60 dias anteriores a data e irá fazer a predição.")

# Campo de seleção de data
selected_date = st.date_input("Selecione uma data", value=date.today())

# Formatar a data como string para a URL (formato YYYY-MM-DD)
date_str = selected_date.strftime("%Y-%m-%d")

# URL base da API
url = "https://qniiuee0ck.execute-api.sa-east-1.amazonaws.com/v1/lambda-model-bitcoin-api"

payload = {
    "date": date_str
}

# Botão
if st.button("Chamar API"):
    
    try:
        # Headers
        headers = {
            "Content-Type": "application/json"
        }

        # Requisição POST
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # levanta erro se status != 200
        data = response.json()
        st.success("Requisição bem-sucedida!")
        st.json(data)  # Exibe o JSON retornado
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao chamar a API: {e}")