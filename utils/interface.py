# utils/interface.py
import streamlit as st
import os
from services.sheets_service import get_dashboard_data
from utils.chatbot import ask_gemini_about_data

# Procure por esta função dentro de utils/interface.py e atualize-a:

def inject_custom_css(is_presentation_mode=False):
    """Injeta o CSS customizado para garantir responsividade e design premium."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", "custom.css")
    css_content = ""
    
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            
    # ALARGADOR DE BARRA LATERAL: Dá espaço físico para o chat de IA não ficar espremido
    css_content += "\n[data-testid='stSidebar'] { min-width: 380px !important; max-width: 380px !important; }\n"
    
    if is_presentation_mode:
        css_content += "\n/* Modo Apresentação */\n"
        css_content += ".block-container { max-width: 100% !important; padding: 1rem 2.5rem !important; }\n"
        
    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

def render_sidebar(show_chat=True):
    """Renderiza a barra lateral completa com logos, status, filtros e o Chatbot Inteligente."""
    # 1. Carregamento dos dados brutos vindos do barramento de dados
    df_raw = get_dashboard_data()
    
    # 2. Renderização Visual da Logo do Instituto Bold
    st.sidebar.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #522f8b; font-weight: 800; margin-bottom: 0; letter-spacing: -1px;">instituto<span style="color:#fb9e21;">bold</span></h2>
            <p style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: #868e96; margin-top: 0;">Programa de Capacitação</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 3. Painel de Status de Sincronização de Dados (Badge Verde)
    total_registros = len(df_raw) if df_raw is not None else 0
    st.sidebar.markdown(
        f"""
        <div style="background-color: rgba(28, 200, 138, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #1cc88a; margin-bottom: 20px;">
            <div style="font-size: 0.8rem; font-weight: bold; color: #1cc88a; text-transform: uppercase;">🟢 Dados Reais Carregados</div>
            <div style="font-size: 0.75rem; color: #495057; margin-top: 5px;"><strong>Planilha:</strong> MASTER (ADM & Bold)</div>
            <div style="font-size: 0.75rem; color: #495057;"><strong>Registros:</strong> {total_registros}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 4. Filtros Estratégicos da Interface
    is_exec_mode = st.sidebar.checkbox("Modo Executivo (Apresentação)", value=False)
    
    status_sel = st.sidebar.selectbox(
        "Filtro de Processamento",
        ["Todos", "Aprovados", "Reprovados"]
    )
    
    # Injeta as regras de estilo de tela dinamicamente
    inject_custom_css(is_exec_mode)
    
    # 5. Motor de Filtragem do Dataframe
    if df_raw is None or df_raw.empty:
        df_filtered = df_raw
    else:
        df_filtered = df_raw.copy()
        if status_sel == "Aprovados":
            df_filtered = df_filtered[df_filtered["status"].astype(str).str.strip().str.lower() == "aprovado"]
        elif status_sel == "Reprovados":
            df_filtered = df_filtered[df_filtered["status"].astype(str).str.strip().str.lower() == "reprovado"]

    # 6. === ASSISTENTE DE CHAT COM IA INTEGRADO (BLINDADO) ===
    if show_chat and df_filtered is not None and not df_filtered.empty:
        st.sidebar.markdown("---")
        with st.sidebar.expander("💬 Assistente IA - Pergunte aos Dados", expanded=False):
            st.markdown("<small style='opacity:0.7;'>Faça perguntas em linguagem natural sobre os dados da planilha.</small>", unsafe_allow_html=True)
            
            # Inicializa o histórico do chat na memória do Streamlit
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            # Exibe mensagens anteriores
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            # Campo de entrada de texto (Input)
            user_query = st.chat_input("Ex: Quantas mulheres de Uberlândia?")
            
            if user_query:
                with st.chat_message("user"):
                    st.write(user_query)
                st.session_state.chat_history.append({"role": "user", "content": user_query})

                # Processa a resposta com o Gemini
                with st.chat_message("assistant"):
                    with st.spinner("Analisando planilha..."):
                        bot_response = ask_gemini_about_data(user_query, df_filtered)
                        st.write(bot_response)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                
                st.rerun()

    return df_filtered, is_exec_mode, status_sel