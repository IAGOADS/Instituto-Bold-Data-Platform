# pages/02_perfil_demografico.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.interface import render_sidebar
from utils.charts import create_gender_chart, create_ethnicity_chart, create_income_chart, COLOR_PALETTE

# 1. FUNÇÃO INTERNA PARA CATEGORIZAÇÃO DAS NOVAS FAIXAS ETÁRIAS
def categorizar_faixa_etaria(idade):
    try:
        id_int = int(float(idade))
        if id_int < 18:
            return "Menos que 18"
        elif 18 <= id_int <= 24:
            return "18 a 24"
        elif 25 <= id_int <= 29:
            return "25 - 29"
        elif 30 <= id_int <= 45:
            return "30 - 45"
        elif 45 <= id_int <= 60:
            return "45 a 60"
        else:
            return "Mais de 60 anos"
    except:
        return "18 a 24"

# Ordem cronológica exata das categorias no gráfico
ORDEM_FAIXAS = ["Menos que 18", "18 a 24", "25 - 29", "30 - 45", "45 a 60", "Mais de 60 anos"]

# Page Config
st.set_page_config(
    page_title="Perfil Demográfico - Instituto Bold & ADM",
    page_icon="👥",
    layout="wide"
)

# Render Sidebar and load filtered data
df_filtered, is_exec_mode, status_sel = render_sidebar()

# Page Title
st.markdown(
    f"""
    <h1 style="color: #522f8b; font-weight: 800; margin-bottom: 0;">PERFIL DEMOGRÁFICO DO PÚBLICO ({status_sel.upper()})</h1>
    <h4 style="color: #004B87; font-weight: 400; margin-top: 0; margin-bottom: 1.5rem;">Análise socioeconômica, geracional e de representatividade</h4>
    """,
    unsafe_allow_html=True
)

if len(df_filtered) == 0:
    st.warning("Sem dados suficientes para gerar as análises demográficas com os filtros selecionados.")
else:
    # Highlights of predominant traits
    st.markdown("<h3 style='color: #522f8b; font-weight: 700; margin-top: 0;'>Características Predominantes</h3>", unsafe_allow_html=True)
    
    col_feat1, col_feat2, col_feat3, col_feat4 = st.columns(4)
    
    pred_age = df_filtered["idade"].mode().iloc[0] if not df_filtered["idade"].empty else "N/A"
    pred_gender = df_filtered["genero"].mode().iloc[0] if not df_filtered["genero"].empty else "N/A"
    pred_income = df_filtered["renda_familiar"].mode().iloc[0] if not df_filtered["renda_familiar"].empty else "N/A"
    pred_ethnic = df_filtered["grupo_etnico"].mode().iloc[0] if not df_filtered["grupo_etnico"].empty else "N/A"
    
    with col_feat1:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-left-color: #fb9e21;">
                <div class="kpi-title">Idade mais Frequente</div>
                <div class="kpi-value kpi-value-gold" style="font-size: 1.8rem;">{pred_age} anos</div>
                <div class="kpi-subtitle">Ponto de maior densidade</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_feat2:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-left-color: #522f8b;">
                <div class="kpi-title">Gênero Majoritário</div>
                <div class="kpi-value kpi-value-purple" style="font-size: 1.8rem;">{pred_gender}</div>
                <div class="kpi-subtitle">Liderança na participação</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_feat3:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-left-color: #004B87;">
                <div class="kpi-title">Renda Familiar Comum</div>
                <div class="kpi-value kpi-value-blue" style="font-size: 1.25rem; line-height: 1.3; font-weight: 800; padding: 4px 0;">{pred_income}</div>
                <div class="kpi-subtitle">Extrato econômico</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_feat4:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-left-color: #1cc88a;">
                <div class="kpi-title">Etnia Predominante</div>
                <div class="kpi-value" style="color: #1cc88a; font-size: 1.8rem;">{pred_ethnic}</div>
                <div class="kpi-subtitle">Distribuição racial</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.write("")
    
    # Linha 1 do Grid: Idade e Gênero
    c_age, c_gender = st.columns([6, 6])
    
    with c_age:
        with st.container(border=True): # Moldura aplicada com sucesso
            df_age = df_filtered.copy()
            df_age["faixa_idade"] = df_age["idade"].apply(categorizar_faixa_etaria)
            
            counts_age = df_age["faixa_idade"].value_counts().reset_index()
            counts_age.columns = ["Faixa Etária", "Quantidade"]
            
            counts_age["Faixa Etária"] = pd.Categorical(counts_age["Faixa Etária"], categories=ORDEM_FAIXAS, ordered=True)
            counts_age = counts_age.sort_values(by="Faixa Etária")
            
            fig_age = px.bar(
                counts_age,
                x="Faixa Etária",
                y="Quantidade",
                color="Faixa Etária",
                title="<b>Distribuição por Faixa Etária (Grupos Geracionais)</b>",
                color_discrete_sequence=COLOR_PALETTE
            )
            fig_age.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=40, t=40, b=40),
                showlegend=False,
                font=dict(family='Outfit', size=11)
            )
            fig_age.update_xaxes(showgrid=False)
            fig_age.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
            st.plotly_chart(fig_age, use_container_width=True)
        
    with c_gender:
        with st.container(border=True): # Moldura aplicada com sucesso
            fig_gender = create_gender_chart(df_filtered)
            st.plotly_chart(fig_gender, use_container_width=True)
        
    # Linha 2 do Grid: Renda e Etnia
    c_income, c_ethnic = st.columns([6, 6])
    
    with c_income:
        with st.container(border=True): # Moldura aplicada com sucesso
            fig_income = create_income_chart(df_filtered)
            st.plotly_chart(fig_income, use_container_width=True)
        
    with c_ethnic:
        with st.container(border=True): # Moldura aplicada com sucesso
            fig_ethnic = create_ethnicity_chart(df_filtered)
            st.plotly_chart(fig_ethnic, use_container_width=True)
        
    # Linha 3 do Grid: Escolaridade
    with st.container(border=True): # Moldura aplicada com sucesso
        st.markdown("<h4 style='margin-top: 0; margin-bottom: 10px; font-weight:700;'>Nível de Escolaridade dos Participantes</h4>", unsafe_allow_html=True)
        
        counts_edu = df_filtered["escolaridade"].value_counts().reset_index()
        counts_edu.columns = ["Escolaridade", "Quantidade"]
        counts_edu = counts_edu.sort_values(by="Quantidade", ascending=True)
        
        fig_edu = px.bar(
            counts_edu,
            x="Quantidade",
            y="Escolaridade",
            orientation="h",
            color="Escolaridade",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig_edu.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=40, t=10, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.20,
                xanchor="center",
                x=0.5
            ),
            font=dict(family='Outfit', size=11)
        )
        fig_edu.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
        fig_edu.update_yaxes(showgrid=False)
        st.plotly_chart(fig_edu, use_container_width=True)