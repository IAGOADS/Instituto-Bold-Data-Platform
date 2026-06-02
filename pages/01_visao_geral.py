# pages/01_visao_geral.py
import io 
import streamlit as st
import pandas as pd
from datetime import datetime
from services.sheets_service import get_dashboard_data
from utils.interface import render_sidebar
from utils.metrics import (
    calculate_kpis, 
    calculate_inclusion_index, 
    calculate_vulnerability_index, 
    calculate_transformation_potential
)
from utils.charts import create_conversion_funnel, create_map_chart
from utils.insights import generate_executive_insights # Importação mantida
from utils.pdf_service import generate_pdf_report

# Page Config
st.set_page_config(page_title="Visão Geral - Impacto Social", page_icon="📊", layout="wide")

# 1. Renderizamos a Sidebar
df_filtered, is_exec_mode, status_sel = render_sidebar()

# 2. Carregamos os dados completos de forma independente para a matemática certa dos KPIs
df_full = get_dashboard_data()

# Títulos Executivos
c_title, c_export = st.columns([7, 3])
with c_title:
    st.markdown(
        """
        <h1 style="color: #522f8b; font-weight: 800; margin-bottom: 0;">VISÃO GERAL DO PROGRAMA</h1>
        <h4 style="color: #004B87; font-weight: 400; margin-top: 0; margin-bottom: 1.5rem;">Storytelling de Impacto, Alcance e Resultados Executivos</h4>
        """,
        unsafe_allow_html=True
    )

# Cálculos rápidos de engine (Carregam na hora)
kpis = calculate_kpis(df_full)
inc_idx = calculate_inclusion_index(df_filtered)
vul_idx = calculate_vulnerability_index(df_filtered)
trans_pot = calculate_transformation_potential(df_filtered)

with c_export:
    st.markdown("<div style='text-align: right; padding-top: 15px;'>", unsafe_allow_html=True)
    pdf_bytes = generate_pdf_report(df_filtered, kpis, inc_idx, vul_idx, trans_pot, ["Insights disponíveis no painel digital."])
    st.download_button(
        label="📥 Exportar PDF Executivo",
        data=pdf_bytes,
        file_name=f"Relatorio_Impacto_Executivo_{status_sel}.pdf",
        mime="application/pdf"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Grid de KPIs executivos (Aparece instantaneamente)
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title" style="white-space:nowrap; font-size:0.85rem;">Inscritos</div><div class="kpi-value kpi-value-blue">{kpis["total_inscritos"]}</div><div class="kpi-subtitle">Candidatos Totais</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title" style="white-space:nowrap; font-size:0.85rem;">Aprovados</div><div class="kpi-value kpi-value-purple">{kpis["total_aprovados"]}</div><div class="kpi-subtitle">Selecionados CAB</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title" style="white-space:nowrap; font-size:0.85rem;">Reprovados</div><div class="kpi-value" style="color:#e74a3b;">{kpis["total_reprovados"]}</div><div class="kpi-subtitle">Filtro Final</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title" style="white-space:nowrap; font-size:0.85rem;">Taxa Aprovação</div><div class="kpi-value kpi-value-gold">{kpis["taxa_aprovacao"]:.1f}%</div><div class="kpi-subtitle">Aproveitamento</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title" style="white-space:nowrap; font-size:0.85rem;">Cidades</div><div class="kpi-value" style="color:#1cc88a;">{kpis["cidades_impactadas"]}</div><div class="kpi-subtitle">Presença Local</div></div>', unsafe_allow_html=True)
with col6:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title" style="white-space:nowrap; font-size:0.85rem;">Estados</div><div class="kpi-value" style="color:#36b9cc;">{kpis["estados_impactados"]}</div><div class="kpi-subtitle">Regiões Atendidas</div></div>', unsafe_allow_html=True)

st.write("")

# Gráficos Dinâmicos Envelopados em Molduras Nativas
c_funnel, c_map = st.columns([5, 7])
with c_funnel:
    with st.container(border=True): # Moldura aplicada no Funil
        st.plotly_chart(create_conversion_funnel(df_full), use_container_width=True, theme="streamlit")

with c_map:
    with st.container(border=True): # Moldura aplicada no Mapa Territorial
        st.markdown("<h4 style='margin-top: 0; margin-bottom: 10px; font-weight:700;'>Abrangência e Densidade Territorial</h4>", unsafe_allow_html=True)
        st.plotly_chart(create_map_chart(df_filtered), use_container_width=True, theme="streamlit")

# 3. Painel de Insights Automáticos com Moldura Adaptável e Spinner Integrado
st.markdown("<h3 style='color: #522f8b; font-weight: 700; margin-top: 1.5rem;'>PAINEL DE INSIGHTS AUTOMÁTICOS</h3>", unsafe_allow_html=True)

with st.container(border=True): # Substituição da div 'insight-box' pela moldura nativa adaptável
    st.markdown("<h4 style='margin-top: 0;'>💡 Destaques Estratégicos Detectados em Tempo Real:</h4>", unsafe_allow_html=True)
    
    # O Spinner atua exclusivamente aqui dentro, protegendo o carregamento visual do cabeçalho e gráficos acima
    with st.spinner("🧠 Conectando ao barramento do Gemini AI... Analisando métricas atuais em tempo real..."):
        insights_list = generate_executive_insights(df_filtered, status_sel == "Aprovados")

    st.markdown("<ul class='insight-list' style='margin-bottom: 0;'>", unsafe_allow_html=True)
    for insight in insights_list:
        st.markdown(f"<li>{insight}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)