# pages/99_diagnostico.py
import streamlit as st
import pandas as pd
from services.sheets_service import connect_to_sheets, test_google_connection, DATA_SOURCE_STATUS, clean_and_map_dataframe
from utils.interface import inject_custom_css

# Page Config
st.set_page_config(
    page_title="Diagnóstico de Integração - Instituto Bold & ADM",
    page_icon="🔧",
    layout="wide"
)

# Inject Custom CSS
inject_custom_css(False)

st.markdown(
    """
    <h1 style="color: #522f8b; font-weight: 800; margin-bottom: 0;">🔧 DIAGNÓSTICO DE INTEGRAÇÃO GOOGLE SHEETS</h1>
    <h4 style="color: #004B87; font-weight: 400; margin-top: 0; margin-bottom: 1.5rem;">Console de auditoria técnica para validação de credenciais, schemas e conexões</h4>
    """,
    unsafe_allow_html=True
)

st.write("")

# Run Connection Test to refresh status
with st.spinner("Realizando auditoria de conexão em tempo real..."):
    success, message = test_google_connection()

# Layout in columns
col_status, col_env = st.columns([5, 7])

with col_status:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #0c2340; margin-top:0; font-weight:700;'>🔌 Status da Conexão</h3>", unsafe_allow_html=True)
    
    if success:
        st.success("🟢 **CONEXÃO OPERACIONAL E REAL**")
        st.markdown(f"**Planilha Carregada:** `{DATA_SOURCE_STATUS['spreadsheet_name']}`")
        st.markdown(f"**Aba Selecionada:** `{DATA_SOURCE_STATUS['worksheet_name']}`")
        st.markdown(f"**Total de Registros (Linhas):** `{DATA_SOURCE_STATUS['total_rows']}`")
        st.markdown(f"**Total de Colunas Mapeadas:** `{DATA_SOURCE_STATUS['total_cols']}`")
    else:
        st.error(f"🔴 **FALHA NA CONEXÃO (DADOS MOCKADOS ATIVOS)**")
        st.markdown(f"**Motivo do Erro:** *{DATA_SOURCE_STATUS['error']}*")
        st.markdown(
            """
            > [!TIP]
            > **Como resolver:**
            > 1. Verifique se o e-mail da Service Account foi compartilhado como **Leitor/Editor** na planilha Google Sheets.
            > 2. Valide se o `GOOGLE_SPREADSHEET_ID` no arquivo `.env` corresponde exatamente ao ID presente na URL da sua planilha.
            > 3. Certifique-se de que a aba da planilha se chama exatamente **CAB**.
            """
        )
    st.markdown("</div>", unsafe_allow_html=True)

with col_env:
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #0c2340; margin-top:0; font-weight:700;'>🔑 Auditoria de Credenciais (.env / Secrets)</h3>", unsafe_allow_html=True)
    
    diag = DATA_SOURCE_STATUS["env_diagnostics"]
    
    # Render table of diagnostics
    diag_data = [
        {"Variável de Ambiente": "Arquivo .env Carregado?", "Status": "✅ SIM" if diag["env_loaded"] else "⚠️ NÃO (Secrets/Gerais)"},
        {"Variável de Ambiente": "GOOGLE_SERVICE_ACCOUNT_EMAIL", "Status": "✅ ENCONTRADO" if diag["email_ok"] else "❌ AUSENTE"},
        {"Variável de Ambiente": "GOOGLE_SPREADSHEET_ID", "Status": "✅ ENCONTRADO" if diag["id_ok"] else "❌ AUSENTE"},
        {"Variável de Ambiente": "GOOGLE_PRIVATE_KEY", "Status": "✅ ENCONTRADO" if diag["key_ok"] else "❌ AUSENTE"},
        {"Variável de Ambiente": "Estrutura PEM da Chave Privada", "Status": "✅ CORRETA" if diag["key_structure_ok"] else "❌ MAL FORMATADA"},
        {"Variável de Ambiente": "Tamanho da Chave Privada", "Status": f"📄 {diag['key_length']} bytes" if diag["key_length"] > 0 else "❌ 0 bytes"}
    ]
    
    st.table(pd.DataFrame(diag_data))
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# 3. Live Data Preview
st.markdown("<h3 style='color: #522f8b; font-weight: 700; margin-top: 1.5rem;'>📋 Pré-visualização dos Dados Originais (Primeiras 10 Linhas)</h3>", unsafe_allow_html=True)

worksheet = connect_to_sheets()
if worksheet is not None:
    try:
        all_records = worksheet.get_all_records()
        if len(all_records) > 0:
            df_preview = pd.DataFrame(all_records).head(10)
            st.dataframe(df_preview, use_container_width=True)
        else:
            st.warning("A aba 'CAB' está conectada, mas não possui registros de dados.")
    except Exception as e:
        st.error(f"Erro ao ler as linhas diretamente do Google Sheets: {e}")
else:
    st.info("💡 Exibindo pré-visualização dos dados simulados (Fallback ativo por ausência de conexão real).")
    from services.sheets_service import generate_synthetic_data
    df_sim_preview = generate_synthetic_data(10)
    st.dataframe(df_sim_preview, use_container_width=True)
