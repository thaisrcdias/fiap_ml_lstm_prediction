# 1. Login na AWS
´´´bash
aws configure
´´´

# 2. Crie o repositório ECR
´´´bash
aws ecr create-repository --repository-name model-bitcoin-lambda
´´´

# 3. Pegue o URI do ECR
´´´bash
123687089814.dkr.ecr.sa-east-1.amazonaws.com/model-bitcoin-lambda
´´´

# 4. Login no Docker com ECR
´´´bash
aws ecr get-login-password | docker login --username AWS --password-stdin 123687089814.dkr.ecr.sa-east-1.amazonaws.com/model-bitcoin-lambda
´´´

# 5. Build da imagem (apenas se não fez a criação da imagem)
´´´bash
docker build -t model-bitcoin-lambda . --provenance=false
´´´

# 6. Tag da imagem para o ECR
´´´bash
docker tag model-bitcoin-lambda:latest 123687089814.dkr.ecr.sa-east-1.amazonaws.com/model-bitcoin-lambda:latest
´´´

# 7. Push
´´´bash
docker push 123687089814.dkr.ecr.sa-east-1.amazonaws.com/model-bitcoin-lambda:latest
´´´

# 8. Teste Local da api no docker
´´´bash
curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{'date': '2025-07-15'}"
´´´

# 9. Criação do lambda
Após subir o container no ECR, criar uma função lambda com imagem via container, selecionar o container criado no ECR.
Em seguida, ajustar os parâmetros de timedout para 3 minutos e a memória máxima para 1GB.

# 10. Criação do API Getway
Crie um API Getway HTTP, vincule com o lambda criado. Selecione o método post e crie uma rota /predict.

# 11. Teste da API
´´´bash
curl -X POST https://qniiuee0ck.execute-api.sa-east-1.amazonaws.com/predict   -H "Content-Type: application/json"   -d '{"date": "2025-07-15"}'
´´´

# 12. Cobrança
| Serviço     | Cobra parado? | Como evitar custo       |
| ----------- | ------------- | ----------------------- |
| ECR         | ✅ Sim         | Exclua imagens antigas  |
| Lambda      | ❌ Não         | Só cobra por invocação  |
| API Gateway | ❌ Não (HTTP)  | Só cobra por requisição |

