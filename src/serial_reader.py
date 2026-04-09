import json
import requests
import time
import random

URL = 'http://localhost:5000/leituras'

def simular_arduino():
    """Gera dados aleatórios simulando o sensor e envia para a API Flask via POST."""
    print("Iniciando simulação do Arduino... Pressione Ctrl+C para parar.")
    
    while True:
        # Gerando valores aleatórios (igual fizemos em C++ no Tinkercad)
        temp = round(random.uniform(20.0, 35.0), 1)
        umid = round(random.uniform(40.0, 80.0), 1)
        
        # Montando o pacote de dados (JSON)
        dados = {
            "temperatura": temp,
            "umidade": umid
        }
        
        try:
            # Enviando os dados para a nossa API no Flask
            resposta = requests.post(URL, json=dados)
            print(f"Enviado: {dados} | Resposta do Servidor: {resposta.status_code}")
        except requests.exceptions.ConnectionError:
            print("Erro: Servidor Flask não está rodando. Ligue o app.py primeiro!")
            
        # Aguarda 5 segundos para a próxima leitura
        time.sleep(5)

if __name__ == '__main__':
    simular_arduino()