# utils/charts.py
import plotly.express as px
import pandas as pd

# 1. PALETA DE CORES CORPORATIVAS (Exigidas pelas páginas)
COLOR_PURPLE = "#522f8b"
COLOR_GOLD = "#fb9e21"
COLOR_BLUE = "#004B87"

# Paleta expandida para gráficos de múltiplas categorias
COLOR_PALETTE = [COLOR_PURPLE, COLOR_GOLD, COLOR_BLUE, "#1cc88a", "#36b9cc", "#9b51e0", "#e74a3b"]

def _aplicar_layout_clean(fig):
    """Função auxiliar para garantir transparência e tipografia Outfit (Light/Dark mode)"""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(family='Outfit', size=11)
    )
    return fig

# ----------------------------------------------------
# GRÁFICOS DA VISÃO GERAL
# ----------------------------------------------------

def create_conversion_funnel(df):
    """Gera o funil de conversão do funil de captação."""
    if df is None or df.empty:
        return px.scatter(title="Sem dados para o Funil")
        
    total = len(df)
    # Tenta normalizar a coluna de status para contagem segura
    status_clean = df["status"].astype(str).str.strip().str.lower() if "status" in df.columns else pd.Series()
    aprovados = (status_clean == "aprovado").sum()
    
    df_funnel = pd.DataFrame({
        "Etapa": ["Inscritos no Funil", "Aprovados (CAB)"],
        "Candidatos": [total, aprovados]
    })
    
    fig = px.funnel(
        df_funnel, 
        y="Etapa", 
        x="Candidatos", 
        title="<b>Funil de Conversão do Programa</b>",
        color_discrete_sequence=[COLOR_PURPLE]
    )
    return _aplicar_layout_clean(fig)

def create_map_chart(df):
    """Gera a distribuição geográfica dos candidatos por Estado/Cidade."""
    if df is None or df.empty:
        return px.scatter(title="Sem dados territoriais")
        
    # Agrupamos por praça para criar a densidade geográfica de forma segura e rápida
    geo_counts = df.groupby(["cidade", "estado"]).size().reset_index(name="Candidatos")
    geo_counts["Localidade"] = geo_counts["cidade"] + " (" + geo_counts["estado"] + ")"
    geo_counts = geo_counts.sort_values(by="Candidatos", ascending=True)
    
    fig = px.bar(
        geo_counts,
        x="Candidatos",
        y="Localidade",
        orientation="h",
        title="<b>Volumetria por Praça Geográfica</b>",
        color_discrete_sequence=[COLOR_BLUE]
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
    return _aplicar_layout_clean(fig)

# ----------------------------------------------------
# GRÁFICOS DO PERFIL DEMOGRÁFICO & APROVADOS
# ----------------------------------------------------

def create_gender_chart(df):
    """Gera o gráfico Donut de distribuição de Gênero."""
    if df is None or df.empty or "genero" not in df.columns:
        return px.scatter(title="Sem dados de Gênero")
        
    counts = df["genero"].value_counts().reset_index()
    counts.columns = ["Gênero", "Quantidade"]
    
    fig = px.pie(
        counts, 
        names="Gênero", 
        values="Quantidade", 
        hole=0.4,
        title="<b>Distribuição por Identidade de Gênero</b>",
        color_discrete_sequence=[COLOR_PURPLE, COLOR_GOLD, COLOR_BLUE]
    )
    return _aplicar_layout_clean(fig)

def create_ethnicity_chart(df):
    """Gera o gráfico de barras de distribuição Étnico-Racial."""
    if df is None or df.empty or "grupo_etnico" not in df.columns:
        return px.scatter(title="Sem dados de Etnia")
        
    counts = df["grupo_etnico"].value_counts().reset_index()
    counts.columns = ["Grupo Étnico", "Quantidade"]
    counts = counts.sort_values(by="Quantidade", ascending=True)
    
    fig = px.bar(
        counts,
        x="Quantidade",
        y="Grupo Étnico",
        orientation="h",
        title="<b>Composição Étnico-Racial (Autoatribuição)</b>",
        color_discrete_sequence=[COLOR_GOLD]
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
    return _aplicar_layout_clean(fig)

def create_income_chart(df):
    """Gera o gráfico de barras horizontais de Renda Familiar."""
    if df is None or df.empty or "renda_familiar" not in df.columns:
        return px.scatter(title="Sem dados de Renda")
        
    counts = df["renda_familiar"].value_counts().reset_index()
    counts.columns = ["Renda Familiar", "Quantidade"]
    counts = counts.sort_values(by="Quantidade", ascending=True)
    
    fig = px.bar(
        counts,
        x="Quantidade",
        y="Renda Familiar",
        orientation="h",
        title="<b>Distribuição Socioeconômica (Renda Familiar)</b>",
        color_discrete_sequence=[COLOR_PURPLE]
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
    return _aplicar_layout_clean(fig)

# ----------------------------------------------------
# GRÁFICOS DE EMPREGABILIDADE & CARREIRA
# ----------------------------------------------------

def create_employability_chart(df):
    """Gera o gráfico de Status Ocupacional/Empregabilidade."""
    if df is None or df.empty or "empregabilidade" not in df.columns:
        return px.scatter(title="Sem dados de Empregabilidade")
        
    counts = df["empregabilidade"].value_counts().reset_index()
    counts.columns = ["Status Profissional", "Quantidade"]
    
    fig = px.pie(
        counts,
        names="Status Profissional",
        values="Quantidade",
        hole=0.4,
        title="<b>Status de Ocupação Atual</b>",
        color_discrete_sequence=COLOR_PALETTE
    )
    return _aplicar_layout_clean(fig)

def create_professional_area_chart(df):
    """Gera o gráfico de áreas de interesse profissional."""
    # Mapeia de forma flexível pelas variações de nomes de coluna comuns
    col = "area_profissional" if "area_profissional" in df.columns else ("area_interesse" if "area_interesse" in df.columns else None)
    if col is None or df is None or df.empty:
        return px.scatter(title="Sem dados de Áreas Profissionais")
        
    counts = df[col].value_counts().reset_index()
    counts.columns = ["Área de Atuação", "Quantidade"]
    counts = counts.sort_values(by="Quantidade", ascending=True)
    
    fig = px.bar(
        counts,
        x="Quantidade",
        y="Área de Atuação",
        orientation="h",
        title="<b>Segmentos e Áreas de Atuação/Interesse</b>",
        color_discrete_sequence=[COLOR_BLUE]
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
    return _aplicar_layout_clean(fig)

def create_experience_chart(df):
    """Gera o gráfico de barras de Tempo de Experiência."""
    col = "tempo_experiencia" if "tempo_experiencia" in df.columns else None
    if col is None or df is None or df.empty:
        return px.scatter(title="Sem dados de Experiência")
        
    counts = df[col].value_counts().reset_index()
    counts.columns = ["Tempo de Experiência", "Quantidade"]
    counts = counts.sort_values(by="Quantidade", ascending=True)
    
    fig = px.bar(
        counts,
        x="Quantidade",
        y="Tempo de Experiência",
        orientation="h",
        title="<b>Tempo de Experiência Profissional Prévio</b>",
        color_discrete_sequence=[COLOR_GOLD]
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
    return _aplicar_layout_clean(fig)

def create_barriers_chart(df):
    """Gera o gráfico de fatores predominantes de risco/barreiras de evasão."""
    # Busca por colunas que mapeiem barreiras ou motivos de evasão no formulário
    col = None
    for c in df.columns:
        if "barreira" in c.lower() or "risco" in c.lower() or "motivo" in c.lower() or "fator" in c.lower():
            col = c
            break
            
    if col is None or df is None or df.empty:
        # Se não encontrar a coluna exata, cria uma distribuição preventiva simulando os fatores do Forms
        return px.scatter(title="Aguardando mapeamento de barreiras estruturais")
        
    counts = df[col].value_counts().reset_index()
    counts.columns = ["Fator de Risco", "Quantidade"]
    counts = counts.sort_values(by="Quantidade", ascending=True)
    
    fig = px.bar(
        counts,
        x="Quantidade",
        y="Fator de Risco",
        orientation="h",
        title="<b>Fatores Predominantes de Risco de Evasão</b>",
        color_discrete_sequence=["#e74a3b"] # Vermelho de atenção corporativa
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
    return _aplicar_layout_clean(fig)