import os
import random
import requests
from dotenv import load_dotenv
import textwrap

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def think(command, name):

    context = textwrap.dedent(f"""
        Você é um assistente virtual inteligente chamado Dusk, amigável e útil.
        Seu objetivo é ajudar o usuário com qualquer dúvida ou tarefa.

        Nome do usuário: {name}

        Comando do usuário: {command}

        Responda de forma clara, concisa, natural e objetiva sendo fácil de entender.
    """)

    response = ask_gemini(context.strip())
    return response

def ask_gemini(question: str) -> str:
    if not API_KEY:
        return "Erro: Chave da API Gemini não configurada."

    try:
        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": question}
                    ]
                }
            ]
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)
        response.raise_for_status()

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        return f"Erro ao se comunicar com a API Gemini: {e}"

def make_response(text: str, name: str, details = "") -> str:

    styles = random.choice([
        "responda com um tom descontraído e natural.",
        "responda indo direto ao ponto, variando a maneira de se expressar.",
        "Responda de forma amigável, mas não tão formal.",
        "Seja simpático, mas sem exageros ou enfeites."
    ])

    prompt = f"""
    Você é Dusk, um assistente virtual amigável e eficiente.

    Usuário: {name}

    {styles}
    {details}

    Transforme a frase a seguir em uma resposta educada, natural e direta, sem repetir informações desnecessárias, e sem frases de introdução.

    Imagine que está conversando naturalmente, sem dar opções ou sugestões.

    Regras:
    - Gere apenas UMA resposta, como se estivesse falando com o usuário naquele instante.
    - Não liste variações, nem retorne múltiplas respostas.
    - Evite respostas muito secas como "ok" ou "feito" isoladas.
    - Não use introduções como "Olá" ou "Oi".

    Frase: "{text}"
    """
    return ask_gemini(prompt.strip())
