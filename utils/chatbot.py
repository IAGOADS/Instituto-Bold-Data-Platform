# utils/chatbot.py
import os
import requests
import json
import streamlit as st

def ask_gemini_about_data(question, df):
    """Envia o dataframe completo + a pergunta do usuário para a API da Perplexity."""
    api_key = os.getenv("PERPLEXITY_API_KEY") or st.secrets.get("PERPLEXITY_API_KEY")

    if not api_key:
        return "⚠️ Chave de API da Perplexity não configurada nos Secrets ou arquivo .env."

    if df is None or df.empty:
        return "A planilha está vazia no momento para análise."

    try:
        url = "https://api.perplexity.ai/chat/completions"
        dados_contexto = df.to_json(orient="records", force_ascii=False)

        payload = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é o Assistente Virtual de Dados do Instituto Bold & ADM. Você tem acesso em tempo real aos dados da planilha de captação de alunos. Responda de forma curta, direta e executiva (máximo 3 frases). Faça os cálculos matemáticos exatos com base nos dados fornecidos (conte linhas, filtre gêneros, etc.). Se não souber ou não estiver nos dados, diga cordialmente que só responde sobre a base de dados do programa."
                },
                {
                    "role": "user",
                    "content": f"Dados atuais da planilha: {dados_contexto}\n\nPergunta do usuário: {question}"
                }
            ],
            "temperature": 0.1
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers, timeout=20)
        
        if response.status_code == 200:
            res_json = response.json()
            return res_json['choices'][0]['message']['content']
        else:
            return f"⚠️ Erro de comunicação com o servidor Perplexity (Código {response.status_code})."

    except Exception as e:
        return f"Erro no motor do chat: {str(e)}"