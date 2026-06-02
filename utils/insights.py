# utils/insights.py
import os
import json
import requests
import pandas as pd
import streamlit as st
from datetime import datetime

def obter_chave_janela_tempo(df):
    now = datetime.now()
    bloco_atual = now.hour // 8
    total_linhas = len(df) if df is not None else 0
    return f"dia_{now.strftime('%Y-%m-%d')}_bloco_{bloco_atual}_linhas_{total_linhas}"

def generate_heuristic_fallback(df, status_txt):
    insights = []
    total = len(df)
    if "cidade" in df.columns and not df["cidade"].empty:
        top_cidade = df["cidade"].value_counts().index[0]
        pct_cidade = (df["cidade"].value_counts().iloc[0] / total) * 100
        insights.append(f"<strong>Distribuição Geográfica:</strong> A maior concentração de inscritos {status_txt} está em <strong>{top_cidade}</strong> ({pct_cidade:.1f}%).")
    if "renda_familiar" in df.columns and not df["renda_familiar"].empty:
        baixa_renda = len(df[df["renda_familiar"].astype(str).str.lower().str.contains("até 1|1 a 2|baixo|mínimo", na=False)])
        pct_baixa = (baixa_renda / total) * 100
        insights.append(f"<strong>Mapeamento Socioeconômico:</strong> O programa registra <strong>{pct_baixa:.1f}%</strong> de perfis de baixa renda elegíveis para impacto social.")
    return insights

@st.cache_data(show_spinner=False)
def _executar_chamada_perplexity_protegida(df_json, status_txt, temporal_key):
    api_key = os.getenv("PERPLEXITY_API_KEY") or st.secrets.get("PERPLEXITY_API_KEY")
    df = pd.read_json(df_json)

    if not api_key:
        return generate_heuristic_fallback(df, status_txt)

    try:
        # Barramento de conexão oficial da Perplexity API
        url = "https://api.perplexity.ai/chat/completions"
        
        total_linhas = len(df)
        cidades = df["cidade"].value_counts().to_dict() if "cidade" in df.columns else {}
        rendas = df["renda_familiar"].value_counts().to_dict() if "renda_familiar" in df.columns else {}
        emprego = df["empregabilidade"].value_counts().to_dict() if "empregabilidade" in df.columns else {}

        resumo_dados = f"Total: {total_linhas}. Cidades: {cidades}. Rendas: {rendas}. Emprego: {emprego}. Filtro atual: {status_txt}."

        payload = {
            "model": "sonar", # Modelo ultra rápido e económico da Perplexity
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um consultor estratégico de BI e ESG. Gere de 3 a 4 insights executivos curtos baseados estritamente nos dados enviados. Retorne apenas os parágrafos de texto, um por linha, sem marcadores de tópicos (*, -, 1.). Use a tag HTML <strong>...</strong> para destacar números importantes."
                },
                {
                    "role": "user",
                    "content": f"Analise estes dados consolidados do programa do Instituto Bold e ADM em Uberlândia: {resumo_dados}"
                }
            ],
            "temperature": 0.2
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Requisição nativa via HTTP POST (Sem necessidade de instalar bibliotecas adicionais)
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code == 200:
            res_json = response.json()
            text_raw = res_json['choices'][0]['message']['content']
            
            linhas = [l.strip() for l in text_raw.split("\n") if l.strip()]
            insights_finais = []
            for linha in linhas:
                if linha.startswith(("- ", "* ", "• ", "1. ", "2. ", "3. ", "4. ", "5. ")):
                    linha = linha.split(" ", 1)[1]
                insights_finais.append(linha)
                
            return insights_finais if insights_finais else generate_heuristic_fallback(df, status_txt)
        else:
            return generate_heuristic_fallback(df, status_txt)
            
    except:
        return generate_heuristic_fallback(df, status_txt)

def generate_executive_insights(df, is_aprovados_only=False):
    if df is None or df.empty:
        return ["Aguardando a entrada de dados para gerar insights."]
        
    status_txt = "selecionados (Aprovados)" if is_aprovados_only else "cadastrados no momento"
    chave_tempo = obter_chave_janela_tempo(df)
    df_json = df.to_json(orient="records", force_ascii=False)
    
    return _executar_chamada_perplexity_protegida(df_json, status_txt, chave_tempo)