# app.py
import streamlit as st
from services.sheets_service import get_dashboard_data # Importação direta da fonte de dados
from utils.interface import render_sidebar
from utils.metrics import calculate_kpis

# 1. CONFIGURAÇÃO PREMIUM DA PÁGINA
st.set_page_config(
    page_title="Instituto Bold & ADM - Dashboard de Impacto Social",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. RENDERIZAÇÃO DA SIDEBAR (Retorna os dados filtrados estáveis)
df_filtered, is_exec_mode, status_sel = render_sidebar()

# 3. BLINDAGEM DOS KPIS: Carrega a base total de forma independente para a página inicial
# Isto garante os números macro estáveis: 14 inscritos totais e 10 aprovados reais.
df_full = get_dashboard_data()
kpis = calculate_kpis(df_full)

# 4. CABEÇALHO EXECUTIVO EM GRADIENTE
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #522f8b 0%, #004B87 100%); padding: 2.5rem; border-radius: 16px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(82, 47, 139, 0.2);">
        <h1 style="margin: 0; font-size: 2.8rem; font-weight: 800; letter-spacing: -0.02em;">PORTAL DE STORYTELLING SOCIAL</h1>
        <h3 style="margin: 5px 0 0 0; font-weight: 400; color: #fb9e21; font-size: 1.3rem;">Demonstração de Impacto, Diversidade e Empregabilidade | Instituto Bold </h3>
        <p style="margin: 15px 0 0 0; font-size: 1rem; opacity: 0.85; max-width: 800px; line-height: 1.6;">
            Bem-vindo ao dashboard executivo desenvolvido para uso do Instituto Bold e da ADM (Archer Daniels Midland). 
            Esta ferramenta foi desenhada no padrão de consultorias estratégicas para transformar dados brutos em uma narrativa viva de impacto social, inclusão e transformação de vidas.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 5. CARDS DE METRICAS GLOBAIS (Refletindo perfeitamente 14 inscritos e 10 aprovados)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title" style="white-space:nowrap; font-size:0.85rem; font-weight:bold;">Inscritos Totais</div>
            <div class="kpi-value kpi-value-blue">{kpis['total_inscritos']}</div>
            <div class="kpi-subtitle">Candidatos no Funil</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title" style="white-space:nowrap; font-size:0.85rem; font-weight:bold;">Aprovados (CAB)</div>
            <div class="kpi-value kpi-value-purple">{kpis['total_aprovados']}</div>
            <div class="kpi-subtitle">Estudantes Ativos</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title" style="white-space:nowrap; font-size:0.85rem; font-weight:bold;">Taxa de Conversão</div>
            <div class="kpi-value kpi-value-gold">{kpis['taxa_aprovacao']:.1f}%</div>
            <div class="kpi-subtitle">Aprovação de Talentos</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title" style="white-space:nowrap; font-size:0.85rem; font-weight:bold;">Cidades Atendidas</div>
            <div class="kpi-value" style="color: #1cc88a;">{kpis['cidades_impactadas']}</div>
            <div class="kpi-subtitle">Abrangência Territorial</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title" style="white-space:nowrap; font-size:0.85rem; font-weight:bold;">Estados Impactados</div>
            <div class="kpi-value" style="color: #36b9cc;">{kpis['estados_impactados']}</div>
            <div class="kpi-subtitle">UF Integrados</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

# 6. CONTEÚDO ADAPTÁVEL AO MODO ESCURO (Cores escuras hardcoded removidas)
c1, c2 = st.columns([7, 5])

with c1:
    st.markdown(
        """
        <div class="metric-container" style="height: 100%;">
            <h3 style="color: #522f8b; margin-top: 0; font-weight: 700;">Nossa Jornada</h3>
            <p style="font-size: 1rem; line-height: 1.6;">
                O <strong>Instituto Bold</strong> investe na aceleração de carreiras de 
                jovens em situação de vulnerabilidade socioeconômica no Brasil. Através de formação em habilidades técnicas e socioemocionais (soft skills), 
                construímos a ponte entre o potencial desses jovens e o mercado corporativo de alta performance.
            </p>
            <h4 style="color: #004B87; font-weight: 600; margin-bottom: 8px;">Estrutura do Dashboard</h4>
            <ul style="padding-left:20px; font-size: 0.95rem; line-height: 1.8;">
                <li><strong>Página 01 - Visão Geral:</strong> Gráficos territoriais, funil de conversão e painel de insights narrativos dinâmicos.</li>
                <li><strong>Página 02 - Perfil Demográfico:</strong> Análise cruzada de idades, etnias, gêneros e renda familiar.</li>
                <li><strong>Página 03 - Impacto Social:</strong> Foco em D&I, incluindo Índices de Inclusão, Vulnerabilidade e Transformação.</li>
                <li><strong>Página 04 - Empregabilidade & Jornada:</strong> Visão profissional dos alunos, capacidade de estudo e barreiras de evasão.</li>
                <li><strong>Página 05 - Consulta Individual:</strong> Busca de perfis específicos por nome, e-mail, LinkedIn, cidade ou status.</li>
                <li><strong>Página 06 - Perfil dos Aprovados:</strong> Relatório consolidado exclusivo de quem foi selecionado no programa.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="metric-container" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h3 style="color: #004B87; margin-top: 0; font-weight: 700;">Status da Conexão</h3>
                <div style="background-color: rgba(40, 167, 69, 0.1); border-left: 4px solid #28a745; padding: 12px; border-radius: 4px; margin-bottom: 15px;">
                    <strong style="color: #28a745; font-size: 0.95rem;">✓ Sincronização Ativa</strong><br>
                    <span style="font-size: 0.85rem;">Os dados do dashboard estão sendo carregados e atualizados diretamente do Google Sheets.</span>
                </div>
                <p style="font-size: 0.9rem; line-height: 1.5; opacity: 0.8;">
                    Utilizamos um barramento de cache inteligente de 10 minutos (TTL) para assegurar o carregamento instantâneo 
                    das páginas sem extrapolar os limites de consumo da API do Google Cloud.
                </p>
            </div>
            <div style="background-color: rgba(128, 128, 128, 0.1); padding: 15px; border-radius: 8px; margin-top: 20px;">
                <span style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; opacity: 0.7; display: block; margin-bottom: 5px;">COMO USAR O MODO APRESENTAÇÃO</span>
                <span style="font-size: 0.85rem; display: block; line-height: 1.4; opacity: 0.9;">
                    Ative a opção <strong>"Modo Executivo (Apresentação)"</strong> na barra lateral ao exibir o painel em reuniões corporativas ou projetores. Isso ocultará botões administrativos e expandirá as dimensões dos gráficos para leitura facilitada.
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )