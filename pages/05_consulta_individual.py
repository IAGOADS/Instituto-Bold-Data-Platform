import streamlit as st
import pandas as pd
from utils.interface import render_sidebar

# Função à prova de falhas para limpar espaços do Markdown
def clean_html(raw_html):
    """Remove todos os espaços no início de cada linha para evitar que o Streamlit crie blocos de código."""
    return "\n".join([line.strip() for line in raw_html.split("\n")])

# Configuração da Página
st.set_page_config(
    page_title="Consulta Individual - Instituto Bold & ADM",
    page_icon="🔍",
    layout="wide"
)

# Renderiza a Sidebar e carrega os dados
df_filtered, is_exec_mode, status_sel = render_sidebar()

# Título da Página
st.markdown(
    clean_html("""
    <h1 style="color: #522f8b; font-weight: 800; margin-bottom: 0;">CONSULTA INDIVIDUAL DE PARTICIPANTES</h1>
    <h4 style="color: #004B87; font-weight: 400; margin-top: 0; margin-bottom: 1.5rem;">Ficha executiva detalhada de talentos, histórias e aspirações</h4>
    """),
    unsafe_allow_html=True
)

if len(df_filtered) == 0:
    st.warning("Sem dados suficientes para realizar consultas com os filtros selecionados.")
else:
    # 1. Painel de Busca
    st.markdown(clean_html("<div class='metric-container'>"), unsafe_allow_html=True)
    st.markdown(clean_html("<h4 style='margin-top:0; margin-bottom:12px; font-weight:700;'>🔎 Filtros de Busca Avançada</h4>"), unsafe_allow_html=True)
    
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    
    with col_s1:
        s_nome = st.text_input("Filtrar por Nome", placeholder="Digite um nome...")
    with col_s2:
        s_email = st.text_input("Filtrar por E-mail", placeholder="Digite um e-mail...")
    with col_s3:
        s_cidade = st.text_input("Filtrar por Cidade", placeholder="Digite uma cidade...")
    with col_s4:
        s_linkedin = st.text_input("Filtrar por LinkedIn", placeholder="Termo no LinkedIn...")
    with col_s5:
        s_status = st.selectbox("Status Processamento", ["Todos", "Aprovado", "Reprovado"], index=0)
        
    st.markdown(clean_html("</div>"), unsafe_allow_html=True)
    
    # 2. Lógica de Filtros
    df_search = df_filtered.copy()
    
    if s_nome:
        df_search = df_search[df_search["nome"].str.contains(s_nome, case=False, na=False)]
    if s_email:
        df_search = df_search[df_search["email"].str.contains(s_email, case=False, na=False)]
    if s_cidade:
        df_search = df_search[df_search["cidade"].str.contains(s_cidade, case=False, na=False)]
    if s_linkedin:
        df_search = df_search[df_search["linkedin"].str.contains(s_linkedin, case=False, na=False)]
    if s_status != "Todos":
        df_search = df_search[df_search["status"] == s_status]
        
    # 3. Exibição da tabela de resultados
    if len(df_search) == 0:
        st.info("Nenhum participante atende aos termos de busca selecionados.")
    else:
        st.markdown(f"**Registros encontrados:** {len(df_search)} participantes.")
        
        # Formata nomes para o menu suspenso
        df_search["display_name"] = df_search.apply(lambda r: f"{r['nome']} ({r['cidade']}-{r['estado']}) | {r['status']}", axis=1)
        
        selected_disp = st.selectbox(
            "Selecione um participante para ver a Ficha Executiva Completa:",
            options=df_search["display_name"].tolist()
        )
        
        # Obtém o registo do participante selecionado
        idx_match = df_search["display_name"].tolist().index(selected_disp)
        candidate = df_search.iloc[idx_match]
        
        st.write("")
        
        # 4. Ficha Executiva Completa (Premium Executive Profile Card)
        status_class = "status-aprovado" if candidate["status"] == "Aprovado" else "status-reprovado"
        
        social_name_html = f"<div style='font-size:0.95rem; margin-top:2px; opacity: 0.8;'>Nome Social: <strong>{candidate['nome_social']}</strong></div>" if candidate['nome_social'] else ""
        
        # O clean_html garante que o HTML não quebra
        st.markdown(
            clean_html(f"""
            <div class="participant-card">
                <div class="participant-header">
                    <div>
                        <div class="participant-name">{candidate['nome'].upper()}</div>
                        {social_name_html}
                        <div style="font-size:0.9rem; color:#004B87; margin-top:4px; font-weight:500;">
                            📧 {candidate['email']} | 📞 {candidate['celular']}
                        </div>
                    </div>
                    <div class="participant-status {status_class}">
                        {candidate['status']}
                    </div>
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )
        
        # Cria as colunas para o layout visual
        col_sec1, col_sec2, col_sec3 = st.columns(3)
        
        with col_sec1:
            st.markdown(
                clean_html(f"""
                <div class="metric-container" style="height: 100%;">
                    <h4 style="color:#522f8b; margin-top:0; border-bottom:1px solid rgba(128,128,128,0.2); padding-bottom:8px; font-weight:700;">👤 Dados Pessoais & D&I</h4>
                    <div class="profile-field-label">Gênero</div>
                    <div class="profile-field-value">{candidate['genero']}</div>
                    <div class="profile-field-label">Grupo Étnico</div>
                    <div class="profile-field-value">{candidate['grupo_etnico']}</div>
                    <div class="profile-field-label">PCD</div>
                    <div class="profile-field-value">{candidate['pcd']}</div>
                    <div class="profile-field-label">Idade</div>
                    <div class="profile-field-value">{candidate['idade']} anos ({candidate['data_nascimento']})</div>
                    <div class="profile-field-label">Renda Familiar</div>
                    <div class="profile-field-value">{candidate['renda_familiar']}</div>
                    <div class="profile-field-label">Pessoas na Residência</div>
                    <div class="profile-field-value">{candidate['pessoas_casa']} moradores</div>
                </div>
                """),
                unsafe_allow_html=True
            )
            
        with col_sec2:
            st.markdown(
                clean_html(f"""
                <div class="metric-container" style="height: 100%;">
                    <h4 style="color:#004B87; margin-top:0; border-bottom:1px solid rgba(128,128,128,0.2); padding-bottom:8px; font-weight:700;">💼 Educação & Carreira</h4>
                    <div class="profile-field-label">Escolaridade</div>
                    <div class="profile-field-value">{candidate['escolaridade']}</div>
                    <div class="profile-field-label">Formação Acadêmica</div>
                    <div class="profile-field-value">{candidate['formacao']} ({candidate['ano_conclusao']})</div>
                    <div class="profile-field-label">Empregabilidade Atual</div>
                    <div class="profile-field-value">{candidate['empregabilidade']}</div>
                    <div class="profile-field-label">Área Profissional</div>
                    <div class="profile-field-value">{candidate['area_profissional']}</div>
                    <div class="profile-field-label">Tempo de Experiência</div>
                    <div class="profile-field-value">{candidate['tempo_experiencia']}</div>
                    <div class="profile-field-label">LinkedIn</div>
                    <div class="profile-field-value"><a href="{candidate['linkedin']}" target="_blank" style="text-decoration:none; font-weight:600;">Ver LinkedIn ↗</a></div>
                </div>
                """),
                unsafe_allow_html=True
            )
            
        with col_sec3:
            st.markdown(
                clean_html(f"""
                <div class="metric-container" style="height: 100%;">
                    <h4 style="color:#fb9e21; margin-top:0; border-bottom:1px solid rgba(128,128,128,0.2); padding-bottom:8px; font-weight:700;">📍 Localidade & Origem</h4>
                    <div class="profile-field-label">Cidade</div>
                    <div class="profile-field-value">{candidate['cidade']}</div>
                    <div class="profile-field-label">Estado (UF)</div>
                    <div class="profile-field-value">{candidate['estado']}</div>
                    <div class="profile-field-label">CEP</div>
                    <div class="profile-field-value">{candidate['cep']}</div>
                    <div class="profile-field-label">Origem da Descoberta</div>
                    <div class="profile-field-value">{candidate['origem_descoberta']}</div>
                </div>
                """),
                unsafe_allow_html=True
            )
            
        st.write("")
        
        # Bloco de Comportamento (Storytelling)
        st.markdown(
            clean_html(f"""
            <div class="metric-container">
                <h4 style="color:#522f8b; margin-top:0; border-bottom:2px solid #522f8b; padding-bottom:8px; font-weight:700;">🧭 Storytelling Qualitativo & Comportamento</h4>
                
                <div style="margin-top: 15px; margin-bottom: 20px;">
                    <strong style="font-size:1rem; display:block;">🧭 Aspiração e Visão de Futuro (O que você espera da Jornada?)</strong>
                    <div style="background-color:rgba(128,128,128,0.1); border-left:4px solid #522f8b; padding:12px; border-radius: 0 8px 8px 0; margin-top:6px; font-size:0.95rem;">
                        "{candidate['expectativa_jornada']}"
                    </div>
                </div>
                
                <div style="margin-bottom: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <strong style="font-size:0.95rem; display:block;">⚠️ Principais Fatores de Risco (Motivos de Evasão)</strong>
                        <div style="background-color:rgba(128,128,128,0.1); border-left:4px solid #e74a3b; padding:10px; border-radius: 0 6px 6px 0; margin-top:4px; font-size:0.9rem;">
                            "{candidate['motivo_desistencia']}"
                        </div>
                    </div>
                    <div>
                        <strong style="font-size:0.95rem; display:block;">📚 Dedicação & Disponibilidade Semanal</strong>
                        <div style="background-color:rgba(128,128,128,0.1); border-left:4px solid #fb9e21; padding:10px; border-radius: 0 6px 6px 0; margin-top:4px; font-size:0.9rem;">
                            Disponibilidade indicada: <strong>{candidate['tempo_dedicacao']}</strong>
                            <br>
                            Evasão prévia em cursos online: <strong>{candidate['historico_conclusao']}</strong>
                        </div>
                    </div>
                </div>
                
                <div>
                    <strong style="font-size:1rem; display:block;">🛠️ Trabalho Recente e Experiência Profissional</strong>
                    <div style="background-color:rgba(128,128,128,0.1); border-left:4px solid #004B87; padding:12px; border-radius: 0 8px 8px 0; margin-top:6px; font-size:0.95rem;">
                        <strong>Trabalho mais próximo de:</strong> {candidate['trabalho_recente']}<br>
                        <strong>Descrição de Experiência:</strong> {candidate['descricao_experiencia']}
                    </div>
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )