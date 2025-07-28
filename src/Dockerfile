FROM public.ecr.aws/lambda/python:3.12

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copia o código
COPY app/ ${LAMBDA_TASK_ROOT}/app

# Define o handler: app/main.py com função lambda_handler
CMD ["app.main.lambda_handler"]
