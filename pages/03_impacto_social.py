# pages/03_impacto_social.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.interface import render_sidebar
from utils.metrics import (
    calculate_inclusion_index,
    calculate_vulnerability_index,
    calculate_transformation_potential
)

# Definição manual das cores da marca para os gráficos
COR_ROXO = "#522f8b"
COR_DOURADO = "#fb9e21"

st.set_page_config(page_title="Impacto Social e ESG - Instituto Bold & ADM", page_icon="🌱", layout="wide")

# Carrega os dados estáveis de 3 variáveis
df_filtered, is_exec_mode, status_sel = render_sidebar()

st.markdown(
    """
    <h1 style="color: #522f8b; font-weight: 800; margin-bottom: 0;">DEMONSTRAÇÃO DE IMPACTO SOCIAL & ESG</h1>
    <h4 style="color: #004B87; font-weight: 400; margin-top: 0; margin-bottom: 1.5rem;">Métricas avançadas de Diversidade, Inclusão e Transformação de Vidas</h4>
    """,
    unsafe_allow_html=True
)

if df_filtered is None or df_filtered.empty:
    st.warning("Sem dados suficientes para gerar os indicadores de impacto com os filtros selecionados.")
else:
    # 1. Cálculos dos Indicadores ESG Estratégicos
    inc_idx = calculate_inclusion_index(df_filtered)
    vul_idx = calculate_vulnerability_index(df_filtered)
    trans_pot = calculate_transformation_potential(df_filtered)

    # Grid Premium de Indicadores Sociais
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div style="background-color: rgba(82, 47, 139, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid {COR_ROXO}; text-align: center;">
            <div style="font-size: 0.9rem; font-weight: bold; color: {COR_ROXO}; text-transform: uppercase;">Índice de Inclusão (D&I)</div>
            <div style="font-size: 2.5rem; font-weight: 800; color: {COR_ROXO}; margin: 10px 0;">{inc_idx:.1f}%</div>
            <div style="font-size: 0.8rem; opacity: 0.85;">Mulheres, negros, indígenas, PCDs e baixa renda contemplados.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div style="background-color: rgba(0, 75, 135, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #004B87; text-align: center;">
            <div style="font-size: 0.9rem; font-weight: bold; color: #004B87; text-transform: uppercase;">Vulnerabilidade Social</div>
            <div style="font-size: 2.5rem; font-weight: 800; color: #004B87; margin: 10px 0;">{vul_idx:.1f}%</div>
            <div style="font-size: 0.8rem; opacity: 0.85;">Participantes expostos a acentuadas barreiras socioeconômicas.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
        <div style="background-color: rgba(251, 158, 33, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid {COR_DOURADO}; text-align: center;">
            <div style="font-size: 0.9rem; font-weight: bold; color: {COR_DOURADO}; text-transform: uppercase;">Potencial de Transformação</div>
            <div style="font-size: 2.5rem; font-weight: 800; color: {COR_DOURADO}; margin: 10px 0;">{trans_pot:.1f}%</div>
            <div style="font-size: 0.8rem; opacity: 0.85;">Jovens desempregados ou em busca do primeiro emprego formal.</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Visualizações adicionais de suporte ao Impacto Social
    g1, g2 = st.columns(2)
    
    with g1:
        if "renda_familiar" in df_filtered.columns:
            with st.container(border=True): # Gráfico envelopado no retângulo moldura nativo
                df_renda = df_filtered["renda_familiar"].value_counts().reset_index()
                df_renda.columns = ["Renda Familiar", "Quantidade"]
                
                # Criado com o tom Roxo da marca
                fig_renda = px.bar(
                    df_renda, 
                    x="Quantidade", 
                    y="Renda Familiar", 
                    orientation="h", 
                    title="<b>Distribuição de Renda Familiar</b>",
                    color_discrete_sequence=[COR_ROXO]
                )
                
                # Limpeza e polimento do layout para Dark/Light Mode
                fig_renda.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=40, t=40, b=40),
                    font=dict(family='Outfit', size=11)
                )
                fig_renda.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
                fig_renda.update_yaxes(showgrid=False)
                
                st.plotly_chart(fig_renda, use_container_width=True, theme="streamlit")
                
    with g2:
        if "pcd" in df_filtered.columns:
            with st.container(border=True): # Gráfico envelopado no retângulo moldura nativo
                df_pcd = df_filtered["pcd"].value_counts().reset_index()
                df_pcd.columns = ["PCD", "Quantidade"]
                
                # Criado usando a combinação de Roxo e Dourado para as fatias
                fig_pcd = px.pie(
                    df_pcd, 
                    names="PCD", 
                    values="Quantidade", 
                    hole=0.4, 
                    title="<b>Inclusão de Pessoas com Deficiência (PCD)</b>",
                    color_discrete_sequence=[COR_ROXO, COR_DOURADO]
                )
                
                # Limpeza e polimento do layout para Dark/Light Mode
                fig_pcd.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=40, t=40, b=40),
                    font=dict(family='Outfit', size=11)
                )
                
                st.plotly_chart(fig_pcd, use_container_width=True, theme="streamlit")