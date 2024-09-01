import os
from pathlib import Path
from dotenv import load_dotenv
import requests

# Carrega as variáveis de ambiente
dotenv_path = Path(__file__).resolve().parent.parent / 'env' / '.env'
if not load_dotenv(dotenv_path=dotenv_path):
    raise Exception(f"Erro ao carregar o arquivo .env em {dotenv_path}")

if load_dotenv(dotenv_path=dotenv_path):
    print(f".env carregado com sucesso em {dotenv_path}")

MARITACA_MODEL = 'sabia-3'

def call_maritaca_api(system_content, user_prompt, max_tokens=100):
    """Call the Maritaca AI API to generate a response based on user input.

    This function sends a request to the Maritaca AI API with the provided system content and user prompt,
    and returns the generated response. It requires a valid API key to be set in the environment variables.

    Args:
        system_content (str): The content that sets the context for the AI response.
        user_prompt (str): The user's input that the AI will respond to.
        max_tokens (int, optional): The maximum number of tokens to generate in the response. Defaults to 100.

    Returns:
        str: The generated response from the Maritaca AI API.

    Raises:
        Exception: If the API key is not found or if there is an error in the API request.
    """
    
    api_key = os.getenv("MARITALK_KEY")
    if not api_key:
        raise Exception("MARITALK_KEY não foi encontrada nas variáveis de ambiente. Por favor verifique seu .env")
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'model': MARITACA_MODEL,
        'messages': [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_prompt}
        ],
        'max_tokens': max_tokens,
    }

    response = requests.post('https://chat.maritaca.ai/api/chat/completions', headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        try:
            error_message = response.json().get('error', {}).get('message', 'Unknown error')
        except:
            error_message = response.text
            raise Exception(f"Erro na solicitação à API da Maritaca AI: {error_message}")
        

def get_car_bio_ai(model, brand, year):
    
    prompt = (
        f"Faça uma descrição de venda de um carro {brand} {model} {year} "
        "em apenas 120 caracteres. Fale coisas específicas da marca e do modelo do carro."
        "Caso não tenha conhecimento do ano do modelo especifico, utilize o conhecimento que você tem até a data atual."
        "Inclua um espaço em branco antes da primeira letra."
    )
    return call_maritaca_api(
        "Você é um especialista em vendas de automóveis.",
        prompt,
        max_tokens=120
    )

def get_car_plate_ai(model, brand, year):  
    prompt = (
        f"Gerar uma placa fictícia para um carro {brand} {model} {year}. "
        "A placa deve seguir o formato padrão Mercosul LLLNLNN. "
        "Gere apenas a placa, sem mais diálogos ou caracteres adicionais."
    )
    return call_maritaca_api(
        "Você é um gerador de informações fictícias para veículos.",
        prompt,
        max_tokens=10
    )

def get_car_value_ai(model, brand, year):  
    prompt = (
        f"Gerar um preço de venda para o carro {brand} {model} {year}. "
        "caso seja necessario gere um  valor baseado em tendências de preços dos modelos anteriores até essa data use apenas numeros"
        "Gere apenas o valor, sem mais diálogos ou caracteres adicionais."
    )
    return call_maritaca_api(
        "Você é um gerador de informações fictícias para veículos.",
        prompt,
        # max_tokens=10
    )
