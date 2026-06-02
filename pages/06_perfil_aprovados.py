# pages/06_perfil_aprovados.py
import streamlit as st
import pandas as pd
import plotly.express as px
from services.sheets_service import get_dashboard_data
from utils.interface import inject_custom_css
from utils.charts import (
    create_gender_chart, 
    create_ethnicity_chart, 
    create_income_chart, 
    create_experience_chart,
    COLOR_PALETTE,
    COLOR_PURPLE,
    COLOR_BLUE,
    COLOR_GOLD
)

# Page Config
st.set_page_config(
    page_title="Perfil dos Aprovados - Instituto Bold & ADM",
    page_icon="🏆",
    layout="wide"
)

# Injeta os estilos customizados padrão do ecossistema
inject_custom_css(False)

# Load data diretamente e filtra exclusivamente para APPROVED
df = get_dashboard_data()
df_aprovados = df[df["status"] == "Aprovado"]

# Page Title
st.markdown(
    """
    <h1 style="color: #522f8b; font-weight: 800; margin-bottom: 0;">🏆 PERFIL EXCLUSIVO DOS APROVADOS</h1>
    <h4 style="color: #004B87; font-weight: 400; margin-top: 0; margin-bottom: 1.5rem;">Análise aprofundada dos talentos selecionados para a jornada CAB</h4>
    """,
    unsafe_allow_html=True
)

if len(df_aprovados) == 0:
    st.warning("Nenhum participante aprovado encontrado na base de dados do Google Sheets.")
else:
    # 1. Cálculos de Métricas Executivas Macro
    total_aprovados = len(df_aprovados)
    median_age = df_aprovados["idade"].median()
    
    # [NOVA MÉTRICA]: Calcula a escolaridade mais frequente (Moda)
    if not df_aprovados["escolaridade"].empty:
        pred_edu = df_aprovados["escolaridade"].mode().iloc[0]
    else:
        pred_edu = "N/A"
    
    # Calcula polo geográfico de maior destaque
    top_city_row = df_aprovados.groupby(["cidade", "estado"]).size().reset_index(name="Count").sort_values(by="Count", ascending=False)
    top_city = f"{top_city_row.iloc[0]['cidade']} ({top_city_row.iloc[0]['estado']})" if not top_city_row.empty else "N/A"
    
    # Grid de KPIs Superiores (Atualizado)
    col_ap1, col_ap2, col_ap3, col_ap4 = st.columns(4)
    
    with col_ap1:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-left-color: #522f8b;">
                <div class="kpi-title">Total de Aprovados</div>
                <div class="kpi-value kpi-value-purple">{total_aprovados}</div>
                <div class="kpi-subtitle">Estudantes ativos na CAB</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_ap2:
        # Substituído: Idade Média deu lugar à Escolaridade mais Frequente com ajuste de fonte seguro
        st.markdown(
            f"""
            <div class="kpi-card" style="border-left-color: #004B87;">
                <div class="kpi-title">Escolaridade Frequente</div>
                <div class="kpi-value kpi-value-blue" style="font-size: 1.2rem; line-height: 1.3; font-weight: 800; padding: 6px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{pred_edu}</div>
                <div class="kpi-subtitle">Nível instrucional predominante</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_ap3:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-left-color: #fb9e21;">
                <div class="kpi-title">Idade Mediana</div>
                <div class="kpi-value kpi-value-gold">{int(median_age)} anos</div>
                <div class="kpi-subtitle">Mediana de idade do grupo</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_ap4:
        st.markdown(
            f"""
            <div class="kpi-card" style="border-left-color: #1cc88a;">
                <div class="kpi-title">Polo de Destaque</div>
                <div class="kpi-value" style="color: #1cc88a; font-size:1.3rem; padding: 5px 0; font-weight:800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{top_city}</div>
                <div class="kpi-subtitle">Maior concentração de alunos</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.write("")
    st.markdown("<p style='font-size:1.05rem; color:#495057; line-height:1.5;'>Abaixo, apresentamos a decomposição estrutural do perfil dos aprovados. Estes dados respondem com precisão sobre a <strong>diversidade socioeconômica, educacional e o perfil profissional</strong> de quem representará a ADM na Jornada CAB.</p>", unsafe_allow_html=True)
    st.write("")
    
    # Abas estruturadas de navegação interna
    tab_demo, tab_socio, tab_carreira = st.tabs(["👥 Demografia de Origem", "🌱 Inclusão & Aspectos Sociais", "💼 Perfil de Carreira"])
    
    # ----------------------------------------------------
    # ABA 1: DEMOGRAFIA DE ORIGEM
    # ----------------------------------------------------
    with tab_demo:
        c_ap_g, c_ap_e = st.columns([6, 6])
        
        with c_ap_g:
            with st.container(border=True):
                fig_g = create_gender_chart(df_aprovados)
                st.plotly_chart(fig_g, use_container_width=True)
            
        with c_ap_e:
            with st.container(border=True):
                fig_e = create_ethnicity_chart(df_aprovados)
                st.plotly_chart(fig_e, use_container_width=True)
            
        # Gráfico Horizontal de Cidades
        with st.container(border=True):
            st.markdown("<h4 style='margin-top: 0; margin-bottom: 10px; font-weight:700;'>Cidades de Origem dos Aprovados</h4>", unsafe_allow_html=True)
            
            c_counts = df_aprovados.groupby(["cidade", "estado"]).size().reset_index(name="Quantidade")
            c_counts["Cidade (UF)"] = c_counts.apply(lambda r: f"{r['cidade']} ({r['estado']})", axis=1)
            c_counts = c_counts.sort_values(by="Quantidade", ascending=True)
            
            fig_c = px.bar(
                c_counts,
                x="Quantidade",
                y="Cidade (UF)",
                orientation="h",
                color_discrete_sequence=[COLOR_PURPLE]
            )
            fig_c.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=40, r=40, t=10, b=40),
                font=dict(family='Outfit', size=11)
            )
            fig_c.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
            st.plotly_chart(fig_c, use_container_width=True)
        
    # ----------------------------------------------------
    # ABA 2: INCLUSÃO & ASPECTOS SOCIAIS
    # ----------------------------------------------------
    with tab_socio:
        c_ap_i, c_ap_ed = st.columns([6, 6])
        
        with c_ap_i:
            with st.container(border=True):
                fig_i = create_income_chart(df_aprovados)
                st.plotly_chart(fig_i, use_container_width=True)
            
        with c_ap_ed:
            with st.container(border=True):
                st.markdown("<h4 style='margin-top: 0; margin-bottom: 10px; font-weight:700;'>Nível Educacional dos Selecionados</h4>", unsafe_allow_html=True)
                
                edu_counts = df_aprovados["escolaridade"].value_counts().reset_index()
                edu_counts.columns = ["Escolaridade", "Quantidade"]
                edu_counts = edu_counts.sort_values(by="Quantidade", ascending=True)
                
                fig_ed = px.bar(
                    edu_counts,
                    x="Quantidade",
                    y="Escolaridade",
                    orientation="h",
                    color_discrete_sequence=[COLOR_GOLD]
                )
                fig_ed.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=40, t=10, b=40),
                    font=dict(family='Outfit', size=11)
                )
                fig_ed.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
                st.plotly_chart(fig_ed, use_container_width=True)
            
    # ----------------------------------------------------
    # ABA 3: PERFIL DE CARREIRA
    # ----------------------------------------------------
    with tab_carreira:
        c_ap_emp, c_ap_area = st.columns([6, 6])
        
        with c_ap_emp:
            with st.container(border=True):
                st.markdown("<h4 style='margin-top: 0; margin-bottom: 10px; font-weight:700;'>Situação de Empregabilidade</h4>", unsafe_allow_html=True)
                
                emp_counts = df_aprovados["empregabilidade"].value_counts().reset_index()
                emp_counts.columns = ["Status", "Quantidade"]
                emp_counts = emp_counts.sort_values(by="Quantidade", ascending=True)
                
                fig_emp = px.bar(
                    emp_counts,
                    x="Quantidade",
                    y="Status",
                    orientation="h",
                    color_discrete_sequence=[COLOR_PURPLE]
                )
                fig_emp.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=40, t=10, b=40),
                    font=dict(family='Outfit', size=11)
                )
                fig_emp.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
                st.plotly_chart(fig_emp, use_container_width=True)
            
        with c_ap_area:
            with st.container(border=True):
                st.markdown("<h4 style='margin-top: 0; margin-bottom: 10px; font-weight:700;'>Áreas de Atuação dos Aprovados</h4>", unsafe_allow_html=True)
                
                area_counts = df_aprovados["area_profissional"].value_counts().reset_index()
                area_counts.columns = ["Área", "Quantidade"]
                area_counts = area_counts.sort_values(by="Quantidade", ascending=True)
                
                fig_area = px.bar(
                    area_counts,
                    x="Quantidade",
                    y="Área",
                    orientation="h",
                    color_discrete_sequence=[COLOR_GOLD]
                )
                fig_area.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=40, t=10, b=40),
                    font=dict(family='Outfit', size=11)
                )
                fig_area.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
                st.plotly_chart(fig_area, use_container_width=True)
            
        # Tempo de Experiência
        with st.container(border=True):
            fig_x = create_experience_chart(df_aprovados)
            st.plotly_chart(fig_x, use_container_width=True)