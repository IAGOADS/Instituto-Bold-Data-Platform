# pages/04_empregabilidade.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.interface import render_sidebar
from utils.charts import (
    COLOR_PALETTE, 
    create_employability_chart, 
    create_professional_area_chart, 
    create_experience_chart, 
    create_barriers_chart
)

# Ordem cronológica das respostas de tempo de dedicação
ORDEM_DEDICACAO = ["Menos de 2 horas", "De 2 a 4 horas", "De 4 a 6 horas", "Mais de 6 horas"]

# Page Config
st.set_page_config(
    page_title="Empregabilidade & Jornada - Instituto Bold & ADM",
    page_icon="💼",
    layout="wide"
)

# Render Sidebar and load filtered data
df_filtered, is_exec_mode, status_sel = render_sidebar()

# Page Title
st.markdown(
    f"""
    <h1 style="color: #522f8b; font-weight: 800; margin-bottom: 0;">EMPREGABILIDADE & JORNADA DO ALUNO ({status_sel.upper()})</h1>
    <h4 style="color: #004B87; font-weight: 400; margin-top: 0; margin-bottom: 1.5rem;">Análise de perfil profissional, de aspirações e comportamento</h4>
    """,
    unsafe_allow_html=True
)

if len(df_filtered) == 0:
    st.warning("Sem dados suficientes para gerar as análises de empregabilidade com os filtros selecionados.")
else:
    # Divisão por abas do Dashboard
    tab_prof, tab_journey = st.tabs(["💼 Perfil Profissional", "🧭 Jornada & Comportamento"])
    
    # ----------------------------------------------------
    # ABA 1: PERFIL PROFISSIONAL
    # ----------------------------------------------------
    with tab_prof:
        st.markdown("<h3 style='color: #522f8b; font-weight: 700; margin-top: 0;'>Perfil Profissional dos Participantes</h3>", unsafe_allow_html=True)
        
        # Linha 1: Gráficos de Empregabilidade e Área Profissional
        c_emp, c_area = st.columns([6, 6])
        
        with c_emp:
            with st.container(border=True): # Gráfico envelopado no retângulo moldura
                fig_emp = create_employability_chart(df_filtered)
                st.plotly_chart(fig_emp, use_container_width=True, theme="streamlit")
            
        with c_area:
            with st.container(border=True): # Gráfico envelopado no retângulo moldura
                fig_area = create_professional_area_chart(df_filtered)
                st.plotly_chart(fig_area, use_container_width=True, theme="streamlit")
            
        # Linha 2: Nível de Experiência e Formação
        c_exp, c_form = st.columns([5, 7])
        
        with c_exp:
            with st.container(border=True):
                fig_exp = create_experience_chart(df_filtered)
                st.plotly_chart(fig_exp, use_container_width=True, theme="streamlit")
            
        with c_form:
            with st.container(border=True):
                st.markdown("<h4 style='margin-top: 0; margin-bottom: 10px; font-weight:700;'>Área de Formação Acadêmica Predominante</h4>", unsafe_allow_html=True)
                
                counts_form = df_filtered["formacao"].value_counts().reset_index()
                counts_form.columns = ["Formação", "Quantidade"]
                counts_form = counts_form.sort_values(by="Quantidade", ascending=True)
                
                fig_form = px.bar(
                    counts_form,
                    x="Quantidade",
                    y="Formação",
                    orientation="h",
                    color_discrete_sequence=[COLOR_PALETTE[1]]
                )
                fig_form.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=40, t=10, b=40),
                    font=dict(family='Outfit', size=11)
                )
                st.plotly_chart(fig_form, use_container_width=True, theme="streamlit")
            
    # ----------------------------------------------------
    # ABA 2: JORNADA & COMPORTAMENTO (Foco da imagem)
    # ----------------------------------------------------
    with tab_journey:
        st.markdown("<h3 style='color: #522f8b; font-weight: 700; margin-top: 0;'>Jornada, Disponibilidade e Barreiras</h3>", unsafe_allow_html=True)
        
        # Linha Superior: Palavras-Chave de Motivação & Card de Evasão
        c_motiv, c_hist = st.columns([7, 5])
        
        with c_motiv:
            with st.container(border=True): # Retângulo envolvendo os badges qualitativos
                st.markdown("<h4 style='margin-top: 0; margin-bottom: 5px; font-weight:700;'>Principais Aspirações (Expectativa de Jornada)</h4>", unsafe_allow_html=True)
                st.markdown("<p style='font-size:0.8rem; color:#868e96; margin-bottom:15px;'>Mapeamento semântico de aspirações e motivações dos estudantes</p>", unsafe_allow_html=True)
                
                # Extração de termos semânticos
                stopwords = {"de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "não", "uma", "os", "as", "no", "na", "mais", "ao", "aos", "me", "se", "por", "como", "ser", "ou", "dos", "das", "esta", "jornada", "curso", "meu", "minha"}
                word_counts = {}
                for text in df_filtered["expectativa_jornada"].dropna().astype(str):
                    words = text.lower().replace(",", "").replace(".", "").replace(";", "").replace("?", "").replace("!", "").split()
                    for word in words:
                        if len(word) > 4 and word not in stopwords:
                            word_counts[word] = word_counts.get(word, 0) + 1
                
                sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:16]
                
                if len(sorted_words) == 0:
                    st.info("Sem dados qualitativos de motivação correspondentes.")
                else:
                    badge_html = "<div style='padding: 10px 0;'>"
                    for word, freq in sorted_words:
                        size_class = "tag-badge-lg" if freq > (sorted_words[0][1] * 0.6) else ""
                        badge_html += f"<span class='tag-badge {size_class}'>{word} <small>({freq})</small></span>"
                    badge_html += "</div>"
                    st.markdown(badge_html, unsafe_allow_html=True)
            
        with c_hist:
            with st.container(border=True): # Retângulo moldura envolvendo o KPI de Evasão de 40%
                st.markdown("<h4 style='margin-top: 0; margin-bottom: 5px; font-weight:700;'>Histórico de Evasão em Cursos Online</h4>", unsafe_allow_html=True)
                st.markdown("<p style='font-size:0.8rem; color:#868e96; margin-bottom:15px;'>Já iniciou outro curso online gratuito e não conseguiu concluir?</p>", unsafe_allow_html=True)
                
                total_linhas = len(df_filtered)
                qtd_sim = df_filtered["historico_conclusao"].astype(str).str.lower().str.contains("sim", na=False).sum()
                yes_pct = (qtd_sim / total_linhas) * 100 if total_linhas > 0 else 0.0
                
                st.markdown(
                    f"""
                    <div style="text-align: center; padding: 20px 0;">
                        <div style="font-size: 3.2rem; font-weight: 800; color: #522f8b; line-height:1;">{yes_pct:.0f}%</div>
                        <strong style="color: #e74a3b; font-size: 1rem; display:block; margin-top:8px;">Já evadiram de cursos gratuitos online</strong>
                        <p style="color: #868e96; font-size: 0.85rem; max-width: 280px; margin: 10px auto 0 auto; line-height: 1.4;">
                            Este número valida a importância do ecossistema de mentorias e acompanhamento individual do Instituto Bold para garantir a conclusão do curso.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
        st.write("")
        
        # Linha Inferior: Gráficos de Dedicação Semanal e Barreiras de Evasão
        c_dedic, c_barr = st.columns([5, 7])
        
        with c_dedic:
            with st.container(border=True): # Retângulo moldura envolvendo o gráfico de barras verticais
                counts_dedic = df_filtered["tempo_dedicacao"].value_counts().reset_index()
                counts_dedic.columns = ["Tempo de Dedicação", "Quantidade"]
                
                counts_dedic["Tempo de Dedicação"] = pd.Categorical(counts_dedic["Tempo de Dedicação"], categories=ORDEM_DEDICACAO, ordered=True)
                counts_dedic = counts_dedic.sort_values(by="Tempo de Dedicação")
                
                fig_dedic = px.bar(
                    counts_dedic,
                    x="Tempo de Dedicação",
                    y="Quantidade",
                    color="Tempo de Dedicação",
                    title="<b>Disponibilidade e Dedicação Semanal Estipulada</b>",
                    color_discrete_sequence=COLOR_PALETTE
                )
                fig_dedic.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=40, t=40, b=40),
                    showlegend=False,
                    font=dict(family='Outfit', size=11)
                )
                fig_dedic.update_xaxes(showgrid=False)
                fig_dedic.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
                st.plotly_chart(fig_dedic, use_container_width=True)
            
        with c_barr:
            with st.container(border=True): # Retângulo moldura envolvendo o gráfico de fatores predominantes
                fig_barr = create_barriers_chart(df_filtered)
                st.plotly_chart(fig_barr, use_container_width=True, theme="streamlit")