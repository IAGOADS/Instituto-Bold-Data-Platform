# services/sheets_service.py
import os
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

# Carrega variáveis de ambiente
env_loaded = load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sheets_service")

DATA_SOURCE_STATUS = {
    "source": "MOCK",
    "error": "Serviço de dados não inicializado",
    "spreadsheet_name": "N/A",
    "worksheet_name": "CAB",
    "total_rows": 0,
    "total_cols": 0,
    "first_cols": [],
    "env_diagnostics": {
        "env_loaded": env_loaded,
        "email_ok": False,
        "key_ok": False,
        "id_ok": False,
        "key_length": 0,
        "key_structure_ok": False
    }
}

COLUMN_MAPPING_LOWER = {
    "carimbo de data/hora": "timestamp",
    "endereço de e-mail": "email",
    "nome completo": "nome",
    "nome social": "nome_social",
    "celular": "celular",
    "cep": "cep",
    "cidade": "cidade",
    "estado": "estado",
    "data de nascimento": "data_nascimento",
    "idade": "idade",
    "grupo étnico": "grupo_etnico",
    "gênero": "genero",
    "renda familiar": "renda_familiar",
    "quantas pessoas moram na sua casa": "pessoas_casa",
    "pcd": "pcd",
    "escolaridade": "escolaridade",
    "empregabilidade": "empregabilidade",
    "área profissional": "area_profissional",
    "tempo de experiência": "tempo_experiencia",
    "linkedin": "linkedin",
    "o que você espera da jornada?": "expectativa_jornada",
    "quanto tempo por semana você consegue dedicar ao curso?": "tempo_dedicacao",
    "você já iniciou outros cursos gratuitos online e não conseguiu concluir?": "historico_conclusao",
    "qual o principal motivo que pode te levar a desistir do curso?": "motivo_desistencia",
    "seu trabalho mais recente é mais próximo de": "trabalho_recente",
    "descreva sua experiência profissional": "descricao_experiencia",
    "como você conheceu o nosso instituto?": "origem_descoberta",
    "formação": "formacao",
    "ano de conclusão": "ano_conclusao",
    "status_processamento": "status"
}

def load_credentials_env():
    """Loads credentials from environment."""
    email = os.getenv("GOOGLE_SERVICE_ACCOUNT_EMAIL")
    private_key = os.getenv("GOOGLE_PRIVATE_KEY")
    spreadsheet_id = os.getenv("GOOGLE_SPREADSHEET_ID")
    
    if not email and "GOOGLE_SERVICE_ACCOUNT_EMAIL" in st.secrets:
        email = st.secrets["GOOGLE_SERVICE_ACCOUNT_EMAIL"]
    if not private_key and "GOOGLE_PRIVATE_KEY" in st.secrets:
        private_key = st.secrets["GOOGLE_PRIVATE_KEY"]
    if not spreadsheet_id and "GOOGLE_SPREADSHEET_ID" in st.secrets:
        spreadsheet_id = st.secrets["GOOGLE_SPREADSHEET_ID"]
        
    if private_key:
        if (private_key.startswith('"') and private_key.endswith('"')) or (private_key.startswith("'") and private_key.endswith("'")):
            private_key = private_key[1:-1]
        private_key = private_key.replace("\\n", "\n")
        
    return email, private_key, spreadsheet_id

def connect_to_sheets():
    """Establishes connection to Google Sheets."""
    email, private_key, spreadsheet_id = load_credentials_env()
    if not email or not private_key or not spreadsheet_id:
        DATA_SOURCE_STATUS["source"] = "MOCK"
        DATA_SOURCE_STATUS["error"] = "Credenciais ausentes no ambiente."
        return None
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials_dict = {
            "type": "service_account",
            "project_id": "dash-adm-bold",
            "private_key": private_key,
            "client_email": email,
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(spreadsheet_id)
        DATA_SOURCE_STATUS["spreadsheet_name"] = spreadsheet.title
        worksheet = spreadsheet.worksheet("CAB")
        return worksheet
    except Exception as e:
        DATA_SOURCE_STATUS["source"] = "MOCK"
        DATA_SOURCE_STATUS["error"] = str(e)
        return None

def test_google_connection():
    worksheet = connect_to_sheets()
    if worksheet is not None:
        try:
            all_records = worksheet.get_all_records()
            DATA_SOURCE_STATUS["source"] = "REAL"
            DATA_SOURCE_STATUS["total_rows"] = len(all_records)
            return True, "Conexão Realizada com Sucesso!"
        except Exception as e:
            return False, str(e)
    return False, DATA_SOURCE_STATUS["error"]

def generate_synthetic_data(num_records=50):
    """Generates safe synthetic data with mathematically normalized probabilities."""
    np.random.seed(42)
    adm_cities = [{"cidade": "Uberlândia", "estado": "MG", "cep": "38400-000"}]
    records = []
    
    # Normalização automática da idade para evitar o ValueError de soma != 1
    idades_possiveis = list(range(18, 36))
    pesos_idade = np.ones(len(idades_possiveis))
    pesos_idade = pesos_idade / pesos_idade.sum() # Força a soma exata de 1.00000
    
    for i in range(num_records):
        city_data = adm_cities[0]
        age = int(np.random.choice(idades_possiveis, p=pesos_idade))
        born_date = (datetime.now() - timedelta(days=age*365)).strftime("%Y-%m-%d")
        
        record = {
            "Carimbo de data/hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Endereço de e-mail": f"aluno{i}@bold.com",
            "Nome completo": f"Estudante Bold Beneficiário {i}",
            "Nome Social": "",
            "CELULAR": "(34) 99999-9999",
            "CEP": city_data["cep"],
            "Cidade": city_data["cidade"],
            "Estado": city_data["estado"],
            "Data de Nascimento": born_date,
            "IDADE": age,
            "Grupo étnico": "Parda",
            "Gênero": "Feminino",
            "Renda Familiar": "Até 1 salário mínimo",
            "Quantas Pessoas moram na sua casa": 3,
            "PCD": "Não",
            "Escolaridade": "Ensino Médio Completo",
            "Empregabilidade": "Desempregado",
            "Área Profissional": "Tecnologia",
            "Tempo de experiência": "Sem experiência",
            "LinkedIn": "https://linkedin.com",
            "O que você espera da Jornada?": "Crescimento profissional",
            "Quanto tempo por semana você consegue dedicar ao curso?": "De 5 a 10 horas",
            "Você já iniciou outros cursos gratuitos online e não conseguiu concluir?": "Não",
            "Qual o principal motivo que pode te levar a desistir do curso?": "Falta de tempo",
            "Seu trabalho mais recente é mais próximo de": "Operacional",
            "Descreva sua experiência profissional": "Apoio operacional",
            "Como você conheceu o nosso Instituto?": "Redes Sociais",
            "FORMAÇÃO": "Ensino Médio Geral",
            "ANO DE CONCLUSÃO": "2022",
            "STATUS_PROCESSAMENTO": "Aprovada" if i % 3 != 0 else "Reprovada"
        }
        records.append(record)
    return pd.DataFrame(records)

@st.cache_data(ttl=600)
def get_dashboard_data():
    """Loads data, prioritizing Google Sheets, falling back safely if needed."""
    worksheet = connect_to_sheets()
    if worksheet is not None:
        try:
            all_records = worksheet.get_all_records()
            if len(all_records) > 0:
                df = pd.DataFrame(all_records)
                DATA_SOURCE_STATUS["source"] = "REAL"
                DATA_SOURCE_STATUS["total_rows"] = len(df)
                DATA_SOURCE_STATUS["total_cols"] = len(df.columns)
                return clean_and_map_dataframe(df)
        except Exception as e:
            logger.error(f"Erro ao ler dados reais: {e}")
            DATA_SOURCE_STATUS["error"] = str(e)
            
    # Se falhar, usa o gerador blindado para não quebrar o dashboard
    DATA_SOURCE_STATUS["source"] = "MOCK"
    return clean_and_map_dataframe(generate_synthetic_data())

def clean_and_map_dataframe(df):
    """Maps fields and handles status cleaning efficiently."""
    df.columns = df.columns.str.strip().str.lower()
    mapped_df = df.rename(columns=COLUMN_MAPPING_LOWER)
    
    if "status" not in mapped_df.columns:
        for col in mapped_df.columns:
            if "status" in col or "processamento" in col or "aprov" in col:
                mapped_df.rename(columns={col: "status"}, inplace=True)
                break

    for friendly_col in COLUMN_MAPPING_LOWER.values():
        if friendly_col not in mapped_df.columns:
            mapped_df[friendly_col] = ""
            
    mapped_df["idade"] = pd.to_numeric(mapped_df["idade"], errors="coerce").fillna(24).astype(int)
    
    # Padronização matemática e definitiva do status
    mapped_df["status"] = mapped_df["status"].astype(str).str.strip().str.lower().apply(
        lambda x: "Reprovado" if "reprov" in x else "Aprovado"
    )
    return mapped_df