# pages/01_visao_geral.py
import io 
import re
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
from datetime import datetime
from services.sheets_service import get_dashboard_data
from utils.interface import render_sidebar
from utils.metrics import (
    calculate_kpis, 
    calculate_inclusion_index, 
    calculate_vulnerability_index, 
    calculate_transformation_potential
)
from utils.charts import create_conversion_funnel
from utils.insights import generate_executive_insights 
from utils.pdf_service import generate_pdf_report

# Page Config
st.set_page_config(page_title="Visão Geral - Impacto Social", page_icon="📊", layout="wide")

# ==============================================================================
# ENGINE DE HIGIENIZAÇÃO E CACHE GEOGRÁFICO CONTRA FALHAS DE INTERNET
# ==============================================================================
COORDENADAS_CIDADES = {
    "Uberlândia": {"lat": -18.9186, "lon": -48.2772, "uf": "MG"},
    "Itapeva": {"lat": -23.9809, "lon": -48.8767, "uf": "SP"},
    "Teresina": {"lat": -5.0919, "lon": -42.8034, "uf": "PI"},
    "Vitória": {"lat": -20.3155, "lon": -40.3128, "uf": "ES"},
    "Vitória Es": {"lat": -20.3155, "lon": -40.3128, "uf": "ES"},
    "Rio De Janeiro": {"lat": -22.9068, "lon": -43.1729, "uf": "RJ"},
    "Salvador": {"lat": -12.9714, "lon": -38.5014, "uf": "BA"}
}

@st.cache_data(ttl=86400)
def higienizar_e_geocodificar_ceps(cep_series):
    """Armazena em cache as consultas de CEP para evitar reprocessamentos inúteis."""
    mapa_cep = {}
    if cep_series is None or cep_series.empty:
        return mapa_cep
    
    ceps_unicos = []
    for val in cep_series.dropna().unique():
        s_val = str(val).strip()
        if s_val.endswith('.0'): s_val = s_val[:-2]
        cep_limpo = re.sub(r"\D", "", s_val)
        if len(cep_limpo) == 8: ceps_unicos.append(cep_limpo)
            
    for cep in set(ceps_unicos):
        try:
            response = requests.get(f"https://cep.awesomeapi.com.br/json/{cep}", timeout=2)
            if response.status_code == 200:
                dados = response.json()
                if "lat" in dados and "lng" in dados:
                    mapa_cep[cep] = {
                        "lat": float(dados.get("lat")),
                        "lon": float(dados.get("lng")),
                        "cidade_correta": dados.get("city", "").title()
                    }
        except:
            pass
    return mapa_cep

# 1. Execução dos barramentos de dados e filtros da Sidebar
df_filtered, is_exec_mode, status_sel = render_sidebar()
df_full = get_dashboard_data()

# ==============================================================================
# PROCESSAMENTO DOS DADOS GEOGRÁFICOS FILTRADOS
# ==============================================================================
col_cep = next((c for c in df_filtered.columns if c.lower() == 'cep'), None)
col_cidade = next((c for c in df_filtered.columns if c.lower() == 'cidade'), None)
col_status = next((c for c in df_filtered.columns if c.lower() == 'status'), None)

if col_cep and not df_filtered.empty:
    dicionario_ceps = higienizar_e_geocodificar_ceps(df_filtered[col_cep])
    
    def obter_lat(val):
        s_val = str(val).strip()
        if s_val.endswith('.0'): s_val = s_val[:-2]
        c = re.sub(r"\D", "", s_val)
        return dicionario_ceps.get(c, {}).get("lat", None)
        
    def obter_lon(val):
        s_val = str(val).strip()
        if s_val.endswith('.0'): s_val = s_val[:-2]
        c = re.sub(r"\D", "", s_val)
        return dicionario_ceps.get(c, {}).get("lon", None)

    df_filtered["latitude"] = df_filtered[col_cep].apply(obter_lat)
    df_filtered["longitude"] = df_filtered[col_cep].apply(obter_lon)
    
    # Aplicação do Fallback local de coordenadas estáveis
    def aplicar_fallback_geo(row):
        lat, lon = row["latitude"], row["longitude"]
        c_nome = str(row[col_cidade]).strip().title() if col_cidade else "Uberlândia"
        if pd.isna(lat) or lat is None:
            for k, v in COORDENADAS_CIDADES.items():
                if k.lower() in c_nome.lower(): return pd.Series([v["lat"], v["lon"]])
        return pd.Series([lat, lon])
        
    df_filtered[["latitude", "longitude"]] = df_filtered.apply(aplicar_fallback_geo, axis=1)
    df_filtered["cidade_corrigida"] = df_filtered[col_cidade].str.title() if col_cidade else "Uberlândia"
else:
    df_filtered["cidade_corrigida"] = df_filtered[col_cidade].str.title() if col_cidade else "Não Informado"
    df_filtered["latitude"] = df_filtered["cidade_corrigida"].apply(lambda x: COORDENADAS_CIDADES.get(x, {}).get("lat", -18.9186))
    df_filtered["longitude"] = df_filtered["cidade_corrigida"].apply(lambda x: COORDENADAS_CIDADES.get(x, {}).get("lon", -48.2772))

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

# Cálculos Estratégicos de KPIs
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

# Grid Executiva de KPIs
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Inscritos</div><div class="kpi-value kpi-value-blue">{kpis["total_inscritos"]}</div><div class="kpi-subtitle">Candidatos Totais</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Aprovados</div><div class="kpi-value kpi-value-purple">{kpis["total_aprovados"]}</div><div class="kpi-subtitle">Selecionados CAB</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Reprovados</div><div class="kpi-value" style="color:#e74a3b;">{kpis["total_reprovados"]}</div><div class="kpi-subtitle">Filtro Final</div></div>', unsafe_allow_html=True)
with col4: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Taxa Aprovação</div><div class="kpi-value kpi-value-gold">{kpis["taxa_aprovacao"]:.1f}%</div><div class="kpi-subtitle">Aproveitamento</div></div>', unsafe_allow_html=True)
with col5: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Cidades</div><div class="kpi-value" style="color:#1cc88a;">{kpis["cidades_impactadas"]}</div><div class="kpi-subtitle">Presença Local</div></div>', unsafe_allow_html=True)
with col6: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Estados</div><div class="kpi-value" style="color:#36b9cc;">{kpis["estados_impactados"]}</div><div class="kpi-subtitle">Regiões Atendidas</div></div>', unsafe_allow_html=True)

st.write("")

# ==============================================================================
# CONFIGURAÇÃO DE LAYOUT INTEGRADO [4, 8] - ALTURA CASADA EM 380PX
# ==============================================================================
ALTURA_FIXA = 380

c_funnel, c_map = st.columns([4, 8])
with c_funnel:
    with st.container(border=True): 
        st.markdown("<h4 style='margin-top: 0; margin-bottom: 10px; font-weight:700;'>Funil de Conversão do Fluxo</h4>", unsafe_allow_html=True)
        fig_fn = create_conversion_funnel(df_full)
        fig_fn.update_layout(height=ALTURA_FIXA)
        st.plotly_chart(fig_fn, use_container_width=True, theme="streamlit")

with c_map:
    with st.container(border=True): 
        st.markdown("<h4 style='margin-top: 0; margin-bottom: 10px; font-weight:700;'>🗺️ Concentração Territorial e Ranking de Municípios por CEP</h4>", unsafe_allow_html=True)
        
        sub_col_mapa, sub_col_grafico = st.columns([1.2, 1])
        df_mapa_valido = df_filtered.dropna(subset=["latitude", "longitude"])
        
        # Consolidação da Tabela de Métricas Municipais
        if not df_mapa_valido.empty:
            def contar_aprovados(x):
                return int(x.astype(str).str.lower().str.contains('aprovado').sum()) if col_status else 0

            df_municipios = df_mapa_valido.groupby("cidade_corrigida").agg(
                latitude=("latitude", "mean"),
                longitude=("longitude", "mean"),
                Inscritos=("cidade_corrigida", "count"),
                Aprovados=(col_status, contar_aprovados) if col_status else ("cidade_corrigida", lambda x: 0)
            ).reset_index()
            df_municipios["Taxa_Aprovação"] = (df_municipios["Aprovados"] / df_municipios["Inscritos"]) * 100
        else:
            df_municipios = pd.DataFrame()

        with sub_col_mapa:
            if not df_municipios.empty:
                # Inicialização do Mapa Folium com tema Dark Friendly de fundo
                m = folium.Map(
                    location=[-14.2350, -51.9253], 
                    zoom_start=3.8, 
                    tiles="cartodbpositron"
                )
                
                # Injeção da Malha de Estados GeoJSON (Fundo Verde Pastel + Borda Cinza)
                geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
                try:
                    folium.GeoJson(
                        geojson_url,
                        name="Divisões Estaduais",
                        style_function=lambda feature: {
                            'fillColor': '#DDEBDD', # Verde pastel suave desejado
                            'color': '#B0B0B0',     # Linhas de divisões estaduais discretas cinzas
                            'weight': 1.2,
                            'fillOpacity': 0.75
                        }
                    ).add_to(m)
                except:
                    pass # Mecanismo de segurança contra instabilidades do GitHub CDN
                
                # Renderização combinada de Clusters e Camada de Calor (HeatMap)
                marker_cluster = MarkerCluster(name="Agrupamentos").add_to(m)
                heat_data = []
                
                for _, row in df_municipios.iterrows():
                    lat, lon = row["latitude"], row["longitude"]
                    cidade = row["cidade_corrigida"]
                    inscritos_qtd = row["Inscritos"]
                    aprovados_qtd = row["Aprovados"]
                    taxa_ap = row["Taxa_Aprovação"]
                    
                    # Pop-up de alta precisão executiva para BI
                    texto_popup = f"""
                    <div style='font-family: sans-serif; font-size:12px; width:200px;'>
                        <b style='color:#522f8b; font-size:14px;'>{cidade}</b><br><hr style='margin:4px 0;'>
                        • <b>Inscritos:</b> {inscritos_qtd}<br>
                        • <b>Aprovados:</b> {aprovados_qtd}<br>
                        • <b>Taxa de Aprovação:</b> {taxa_ap:.1f}%
                    </div>
                    """
                    
                    # Alimenta os dados de densidade do mapa de calor
                    heat_data.append([lat, lon, float(inscritos_qtd)])
                    
                    # Marcadores personalizados com as Cores Institucionais Bold (Roxo e Doutado)
                    cor_marcador = "#522f8b" if inscritos_qtd > 5 else "#fb9e21"
                    folium.CircleMarker(
                        location=[lat, lon],
                        radius=8 + (float(inscritos_qtd) * 0.4),
                        popup=folium.Popup(texto_popup, max_width=250),
                        color=cor_marcador,
                        fill=True,
                        fill_color=cor_marcador,
                        fill_opacity=0.85
                    ).add_to(marker_cluster)
                
                # Mescla a intensidade visual do HeatMap ao ecossistema do mapa
                HeatMap(heat_data, radius=25, blur=15, min_opacity=0.4).add_to(m)
                
                # Renderização final controlada do componente de mapa
                st_folium(m, height=ALTURA_FIXA, use_container_width=True, key="brazil_corporate_map")
            else:
                st.info("Aguardando consolidação geográfica dos registros.")

        with sub_col_grafico:
            if not df_municipios.empty:
                # Ordenação decrescente precisa para gerar o ranking executivo
                df_ranking = df_municipios.sort_values(by="Inscritos", ascending=True)
                
                fig_barras = px.bar(
                    df_ranking,
                    x="Inscritos",
                    y="cidade_corrigida",
                    orientation="h",
                    text="Inscritos",
                    color="Inscritos",
                    # Escala cromática de transição oficial: do Dourado ao Roxo Bold
                    color_continuous_scale=["#fb9e21", "#522f8b"]
                )
                fig_barras.update_layout(
                    showlegend=False,
                    coloraxis_showscale=False,
                    height=ALTURA_FIXA,
                    margin={"r": 15, "t": 0, "l": 10, "b": 10},
                    xaxis_title=None,
                    yaxis_title=None
                )
                fig_barras.update_traces(textposition="outside", cliponaxis=False)
                st.plotly_chart(fig_barras, use_container_width=True, theme="streamlit")
            else:
                st.write("<div style='padding-top:50px; text-align:center; color:gray;'>Sem dados cadastrados.</div>", unsafe_allow_html=True)

# 3. Painel de Insights Automáticos
st.markdown("<h3 style='color: #522f8b; font-weight: 700; margin-top: 1.5rem;'>PAINEL DE INSIGHTS AUTOMÁTICOS</h3>", unsafe_allow_html=True)
with st.container(border=True): 
    st.markdown("<h4 style='margin-top: 0;'>💡 Destaques Estratégicos Detectados em Tempo Real:</h4>", unsafe_allow_html=True)
    with st.spinner("🧠 Processando barramento analítico de dados..."):
        insights_list = generate_executive_insights(df_filtered, status_sel == "Aprovados")

    for insight in insights_list:
        insight_limpo = insight.replace("<strong>", "**").replace("</strong>", "**").replace("<li>", "").replace("</li>", "")
        st.markdown(f"• {insight_limpo}")