# utils/chatbot.py
import os
import requests
import json
import streamlit as st
import pandas as pd
from services.sheets_service import get_dashboard_data

def ask_gemini_about_data(question, df):
    """Mecanismo analítico puro que higieniza os dados e calcula as regras de 
    elegibilidade oficiais de forma exata na memória, eliminando falsos positivos.
    """
    api_key = os.getenv("PERPLEXITY_API_KEY") or st.secrets.get("PERPLEXITY_API_KEY")

    if not api_key:
        return "⚠️ Chave de API da Perplexity não configurada nos Secrets ou arquivo .env."

    # Força carregar a planilha master para garantir que o chat tenha acesso a todas as linhas vivas
    df_master = get_dashboard_data()
    df_alvo = df_master if (df_master is not None and not df_master.empty) else df

    if df_alvo is None or df_alvo.empty:
        return "A planilha está vazia no momento para análise."

    try:
        url = "https://api.perplexity.ai/chat/completions"
        df_ia = df_alvo.copy()
        
        # --- FILTRO DE SEGURANÇA (REMOVE CAMPOS DE TEXTO LIVRE QUE ACUMULAM TOKENS) ---
        colunas_para_excluir = ["O que você espera da Jornada?", "Descreva sua experiência profissional", "O que você espera da Jornada"]
        for col in df_ia.columns:
            if "Autorizo gratuitamente" in str(col) or len(str(col)) > 100:
                colunas_para_excluir.append(col)
        df_ia = df_ia.drop(columns=[c for c in colunas_para_excluir if c in df_ia.columns], errors="ignore")
        
        # --- NORMALIZAÇÃO PADRÃO DE CABEÇALHOS ---
        df_ia.columns = df_ia.columns.str.strip().str.replace(r'[.:?"]', '', regex=True).str.replace(' ', '_').str.upper()
        
        # --- DETECÇÃO CRÍTICA DE COLUNAS DE DIRETRIZES ---
        col_genero = next((c for c in df_ia.columns if 'GÊN' in c or 'GEN' in c), None)
        col_cidade = next((c for c in df_ia.columns if 'CIDADE' in c or 'MUNICI' in c), None)
        col_renda = next((c for c in df_ia.columns if 'RENDA' in c or 'SALÁ' in c or 'SALAR' in c), None)

        total_inscritos = len(df_ia)
        total_aprovados = 0
        total_reprovados = 0
        
        inscritos_uberlandia = 0
        inscritos_mulheres = 0
        inscritos_homens = 0
        
        cidade_errada = 0
        renda_alta = 0
        genero_errado = 0
        multiplos = 0
        
        # --- 🧠 PROCESSAMENTO LÓGICO SELETIVO EM PYTHON ---
        for _, row in df_ia.iterrows():
            falhas = []
            
            # 1. Auditoria Fina de Cidade
            if col_cidade:
                cid = str(row[col_cidade]).upper().strip()
                if 'UBERLANDIA' in cid or 'UBERLÂNDIA' in cid:
                    inscritos_uberlandia += 1
                else:
                    falhas.append('cidade')
            else:
                falhas.append('cidade')
                
            # 2. Auditoria Fina de Gênero
            if col_genero:
                gen = str(row[col_genero]).upper().strip()
                if 'FEM' in gen or 'MULHER' in gen or gen == 'F':
                    inscritos_mulheres += 1
                else:
                    inscritos_homens += 1
                    falhas.append('genero')
            else:
                falhas.append('genero')
                
            # 3. Auditoria Fina de Renda Familiar (Apenas a palavra 'ACIMA' gera reprovação)
            if col_renda:
                ren = str(row[col_renda]).upper().strip()
                if 'ACIMA' in ren:
                    falhas.append('renda')
            
            # Contabilização Real dos Resultados de Cockpit
            if len(falhas) == 0:
                total_aprovados += 1
            else:
                total_reprovados += 1
                if len(falhas) > 1:
                    multiplos += 1
                elif falhas[0] == 'cidade':
                    cidade_errada += 1
                elif falhas[0] == 'genero':
                    genero_errado += 1
                elif falhas[0] == 'renda':
                    renda_alta += 1

        dados_planilha_texto = df_ia.to_csv(index=False)
        colunas_disponiveis = ", ".join(df_ia.columns)

        # Injeção Exata das Métricas Reais no Prompt de Sistema
        bloco_auditoria_python = f"""
---
VERDADE MATEMÁTICA DA PLANILHA (CALCULADA EM TEMPO REAL):
- Total Geral de Inscritos Carregados: {total_inscritos}
- Total de Candidatos Aprovados/Elegíveis: {total_aprovados}
- Total de Candidatos Reprovados/Não Elegíveis: {total_reprovados}

ESTATÍSTICAS GERAIS DE CADASTRO:
• Total de Inscritos de Uberlândia: {inscritos_uberlandia}
• Total de Inscritos do gênero Feminino (Mulheres): {inscritos_mulheres}
• Total de Inscritos do gênero Masculino (Homens): {inscritos_homens}

SEGMENTAÇÃO EXCLUSIVA POR CLUSTERS DE REPROVAÇÃO (CAUSA RAIZ REAL):
Dos {total_reprovados} candidatos reprovados na base:
• {cidade_errada} foram reprovados unicamente por não residirem em Uberlândia.
• {renda_alta} foram reprovados unicamente por possuírem renda familiar "Acima de 4 salários mínimos".
• {genero_errado} foram reprovados unicamente por não pertencerem ao gênero feminino.
• {multiplos} foram reprovados por acumularem múltiplos critérios de descumprimento simultâneos.
---
"""

        # ==============================================================================
        # ENGENHARIA DE PROMPT MESTRE REFINADO
        # ==============================================================================
        system_prompt = f"""Você é o Assistente Virtual de Dados do Instituto Bold & ADM.
Sua única fonte de informação é a planilha de inscrições carregada no sistema anexada abaixo em formato CSV. Responda exclusivamente com base nos dados e na auditoria fornecida abaixo.

{bloco_auditoria_python}

COLUNAS DISPONÍVEIS NA BASE:
[{colunas_disponiveis}]

DADOS REAIS DA PLANILHA (FORMATO CSV):
{dados_planilha_texto}

Regras de Resposta
- Responda de forma objetiva, executiva e direta.
- Quando o usuário perguntar o número de aprovados, reprovados, inscritos de Uberlândia ou os motivos/porquês das reprovações, você DEVE utilizar EXATAMENTE os dados fornecidos na seção "VERDADE MATEMÁTICA DA PLANILHA", "ESTATÍSTICAS GERAIS DE CADASTRO" e "SEGMENTAÇÃO EXCLUSIVA POR CLUSTERS DE REPROVAÇÃO" acima. Nunca tente adivinhar ou recalcular, confie na auditoria do Python.
- Apresente os motivos de reprovação em tópicos claros (bullets).
- Nunca invente informações ou mude as contagens fornecidas na verdade matemática acima.
"""

        payload = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Pergunta: {question}"}
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